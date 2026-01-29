import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from pinecone import Pinecone, ServerlessSpec
import time

# Page configuration
st.set_page_config(
    page_title="Chat with PDFs",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'processed' not in st.session_state:
    st.session_state.processed = False

def get_pdf_text(pdf_docs):
    """Extract text from uploaded PDF documents"""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    """
    Split text into chunks using RecursiveCharacterTextSplitter
    Strategy: 1000 char chunks with 200 char overlap for context preservation
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks, api_key, pinecone_api_key):
    """
    Create vector store using Pinecone
    Uses OpenAI embeddings (text-embedding-ada-002)
    """
    # Initialize Pinecone
    pc = Pinecone(api_key=pinecone_api_key)
    
    index_name = "pdf-chat-index"
    
    # Check if index exists, if not create it
    existing_indexes = [index.name for index in pc.list_indexes()]
    
    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=1536,  # OpenAI embedding dimension
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        # Wait for index to be ready
        time.sleep(1)
    
    # Initialize embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    
    # Create vector store
    vectorstore = PineconeVectorStore.from_texts(
        texts=text_chunks,
        embedding=embeddings,
        index_name=index_name
    )
    
    return vectorstore

def get_conversation_chain(vectorstore, api_key):
    """
    Create conversational retrieval chain with memory
    Uses GPT-3.5-turbo for cost efficiency
    """
    llm = ChatOpenAI(
        openai_api_key=api_key,
        model_name="gpt-3.5-turbo",
        temperature=0.7
    )
    
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True,
        output_key='answer'
    )
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        return_source_documents=True
    )
    
    return conversation_chain

def handle_userinput(user_question):
    """Handle user questions and display chat history"""
    if st.session_state.conversation is None:
        st.warning("Please upload and process PDFs first!")
        return
    
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history.append({
        'question': user_question,
        'answer': response['answer']
    })
    
    # Display chat history
    for i, message in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.write(message['question'])
        with st.chat_message("assistant"):
            st.write(message['answer'])

def main():
    st.title("📚 Chat with PDFs using RAG")
    st.markdown("Upload PDF documents and ask questions about their content!")
    
    # Sidebar for API keys and PDF upload
    with st.sidebar:
        st.header("Configuration")
        
        openai_api_key = st.text_input("OpenAI API Key", type="password", 
                                       help="Get your API key from platform.openai.com")
        pinecone_api_key = st.text_input("Pinecone API Key", type="password",
                                         help="Get your API key from app.pinecone.io")
        
        st.header("Upload Documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here",
            accept_multiple_files=True,
            type=['pdf']
        )
        
        if st.button("Process Documents"):
            if not openai_api_key or not pinecone_api_key:
                st.error("Please provide both API keys!")
            elif not pdf_docs:
                st.error("Please upload at least one PDF!")
            else:
                with st.spinner("Processing documents..."):
                    try:
                        # Extract text
                        raw_text = get_pdf_text(pdf_docs)
                        
                        # Create chunks
                        text_chunks = get_text_chunks(raw_text)
                        st.info(f"Created {len(text_chunks)} text chunks")
                        
                        # Create vector store
                        vectorstore = get_vectorstore(text_chunks, openai_api_key, pinecone_api_key)
                        
                        # Create conversation chain
                        st.session_state.conversation = get_conversation_chain(vectorstore, openai_api_key)
                        st.session_state.processed = True
                        
                        st.success("Documents processed successfully! You can now ask questions.")
                    except Exception as e:
                        st.error(f"Error processing documents: {str(e)}")
        
        if st.session_state.processed:
            st.success("✅ Documents are ready for chat!")
        
        # Info section
        st.markdown("---")
        st.markdown("### About This App")
        st.markdown("""
        This app uses:
        - **OpenAI GPT-3.5** for responses
        - **Pinecone** for vector storage
        - **RAG** for context-aware answers
        - **LangChain** for orchestration
        """)
    
    # Main chat interface
    st.markdown("### Ask questions about your documents")
    
    user_question = st.chat_input("Ask a question about your PDFs...")
    
    if user_question:
        handle_userinput(user_question)
    
    # Display instructions if not processed
    if not st.session_state.processed:
        st.info("👈 Upload your PDFs and provide API keys in the sidebar to get started!")

if __name__ == '__main__':
    main()
