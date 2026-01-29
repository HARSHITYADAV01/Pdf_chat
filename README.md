# 📚 Chat with PDFs - RAG-Powered AI Prototype

A production-ready AI application that allows users to upload PDF documents and interact with them through natural language conversations using Retrieval-Augmented Generation (RAG).

## 🎯 Project Overview

This prototype demonstrates practical implementation of:
- **Large Language Models (LLMs)** - OpenAI GPT-3.5-turbo
- **Retrieval-Augmented Generation (RAG)** - Context-aware responses
- **Vector Embeddings** - OpenAI text-embedding-ada-002
- **Vector Database** - Pinecone for semantic search
- **Intelligent Chunking** - Recursive text splitting with overlap
- **Prompt Engineering** - Conversational retrieval chain
- **User Interface** - Streamlit for interactive experience

## 🏗️ Architecture & Design Decisions

### 1. RAG Pipeline Architecture

```
PDF Upload → Text Extraction → Chunking → Embeddings → Vector Store → Retrieval → LLM → Response
```

### 2. Chunking Strategy

**Choice: RecursiveCharacterTextSplitter**
- **Chunk Size**: 1000 characters
- **Overlap**: 200 characters
- **Rationale**: 
  - 1000 chars provides sufficient context while staying within token limits
  - 200 char overlap prevents loss of context at chunk boundaries
  - Recursive splitting respects natural text boundaries (paragraphs, sentences, words)

### 3. LLM Selection

**Primary Model: GPT-3.5-turbo**
- Cost-effective for production use
- Fast response times
- Sufficient capability for Q&A tasks
- Temperature: 0.7 (balanced creativity and accuracy)

### 4. Embedding Model

**OpenAI text-embedding-ada-002**
- 1536-dimensional vectors
- Optimized for semantic search
- Cost-effective ($0.0001 per 1K tokens)
- Industry-standard performance

### 5. Vector Database

**Pinecone (Serverless)**
- Free tier: 1 index, 100K vectors
- Low latency semantic search
- No infrastructure management
- Cosine similarity for relevance

### 6. Retrieval Strategy

**Top-K Retrieval**: k=3
- Returns 3 most relevant chunks
- Balances context richness with token efficiency
- Reduces hallucination risk

### 7. Memory Management

**ConversationBufferMemory**
- Maintains full chat history
- Enables follow-up questions
- Context-aware conversations

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenAI API account (free tier available)
- Pinecone API account (free tier available)

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd pdf-chat-rag
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Get API Keys

#### OpenAI API Key
1. Visit [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create new secret key
5. Copy the key (keep it secure!)

**Free Tier**: $5 credit for new users

#### Pinecone API Key
1. Visit [app.pinecone.io](https://app.pinecone.io)
2. Sign up for free account
3. Create a new project
4. Go to API Keys section
5. Copy your API key

**Free Tier**: 
- 1 index
- 100K vectors (~100 documents)
- Serverless deployment

### Step 5: Run the Application

```bash
streamlit run pdf_chat_app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

1. **Enter API Keys**
   - Paste your OpenAI API key in the sidebar
   - Paste your Pinecone API key in the sidebar

2. **Upload PDFs**
   - Click "Browse files" in the sidebar
   - Select one or more PDF files
   - Click "Process Documents"

3. **Wait for Processing**
   - The app will extract text from PDFs
   - Create intelligent chunks
   - Generate embeddings
   - Store in Pinecone vector database

4. **Start Chatting**
   - Type your question in the chat input
   - Get AI-powered answers based on your documents
   - Ask follow-up questions for deeper understanding

## 🛠️ Technologies Used

### Core Libraries

| Library | Purpose | Version |
|---------|---------|---------|
| **Streamlit** | Web UI framework | 1.31.0 |
| **LangChain** | LLM orchestration | 0.1.9 |
| **OpenAI** | LLM & embeddings | 1.12.0 |
| **Pinecone** | Vector database | 3.0.3 |
| **PyPDF2** | PDF text extraction | 3.0.1 |

### Key Components

1. **Text Extraction**: PyPDF2
2. **Text Splitting**: RecursiveCharacterTextSplitter
3. **Embeddings**: OpenAIEmbeddings
4. **Vector Store**: PineconeVectorStore
5. **LLM**: ChatOpenAI (GPT-3.5-turbo)
6. **Chain**: ConversationalRetrievalChain
7. **Memory**: ConversationBufferMemory

## 🎨 Features

✅ **Multi-PDF Support** - Upload and process multiple documents simultaneously  
✅ **Semantic Search** - Find relevant information using natural language  
✅ **Conversational Memory** - Ask follow-up questions with context  
✅ **Smart Chunking** - Intelligent text splitting preserves context  
✅ **Source Tracking** - Responses based on actual document content  
✅ **Real-time Processing** - Instant feedback on document processing  
✅ **Error Handling** - Graceful handling of API errors and edge cases  

## 🔧 Advanced Configuration

### Adjusting Chunk Size

In `pdf_chat_app.py`, modify the `get_text_chunks()` function:

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,  # Increase for longer contexts
    chunk_overlap=300,  # Increase overlap for better continuity
    length_function=len
)
```

### Changing Retrieval Count

Modify the `get_conversation_chain()` function:

```python
retriever=vectorstore.as_retriever(search_kwargs={"k": 5})  # Retrieve top 5 chunks
```

### Upgrading to GPT-4

```python
llm = ChatOpenAI(
    openai_api_key=api_key,
    model_name="gpt-4",  # Better accuracy, higher cost
    temperature=0.7
)
```

## 💡 Prompt Engineering

The app uses LangChain's `ConversationalRetrievalChain` which implements sophisticated prompt engineering:

1. **System Prompt**: Instructs the model to answer based on provided context
2. **Context Injection**: Relevant document chunks are automatically added
3. **Chat History**: Previous messages provide continuity
4. **Answer Synthesis**: Model combines retrieved context with its knowledge

## 🔒 Security Best Practices

- ⚠️ **Never commit API keys** to version control
- ✅ Use environment variables for production
- ✅ Implement rate limiting for API calls
- ✅ Validate and sanitize PDF inputs
- ✅ Use HTTPS in production deployments

## 📊 Cost Estimation (Free Tier)

### OpenAI
- **Embeddings**: ~$0.0001 per 1K tokens
- **GPT-3.5**: ~$0.002 per 1K tokens
- **Example**: 100-page PDF ≈ $0.50-$2.00

### Pinecone
- **Free Tier**: Completely free for up to 100K vectors
- **No credit card required**

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution**: Make sure virtual environment is activated and dependencies installed

### Issue: "Invalid API key"
**Solution**: Check your API keys are correct and active

### Issue: "Index already exists"
**Solution**: The app reuses the existing index. To reset, delete the index in Pinecone console

### Issue: "Rate limit exceeded"
**Solution**: OpenAI free tier has limits. Wait a few minutes or upgrade plan

## 🚢 Deployment Options

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect repository
4. Add API keys as secrets
5. Deploy!

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "pdf_chat_app.py"]
```

## 📈 Future Enhancements

- [ ] Support for multiple file formats (DOCX, TXT, CSV)
- [ ] Document summarization feature
- [ ] Citation and source highlighting
- [ ] Multi-language support
- [ ] User authentication
- [ ] Document collections management
- [ ] Export chat history
- [ ] Advanced filtering options

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project for learning and development.

## 👤 Author

Created as part of an LLM-powered AI prototype assessment.

---

**Note**: This is a prototype for educational purposes. For production use, implement proper authentication, error handling, and monitoring.
