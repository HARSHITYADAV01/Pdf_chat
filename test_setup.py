"""
Test script to validate the PDF Chat RAG setup
Run this to check if all dependencies are installed correctly
"""

import sys

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher required")
        return False
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = {
        'streamlit': 'Streamlit',
        'PyPDF2': 'PyPDF2',
        'langchain': 'LangChain',
        'langchain_openai': 'LangChain OpenAI',
        'langchain_pinecone': 'LangChain Pinecone',
        'pinecone': 'Pinecone',
        'openai': 'OpenAI',
        'tiktoken': 'TikToken',
        'dotenv': 'python-dotenv'
    }
    
    all_installed = True
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {name} installed")
        except ImportError:
            print(f"❌ {name} NOT installed")
            all_installed = False
    
    return all_installed

def check_environment():
    """Check for environment variables"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    pinecone_key = os.getenv('PINECONE_API_KEY')
    
    if openai_key:
        print(f"✓ OpenAI API key found in environment")
    else:
        print("⚠ OpenAI API key not found (can be entered in UI)")
    
    if pinecone_key:
        print(f"✓ Pinecone API key found in environment")
    else:
        print("⚠ Pinecone API key not found (can be entered in UI)")

def main():
    print("=" * 50)
    print("PDF Chat RAG - Setup Validation")
    print("=" * 50)
    print()
    
    print("Checking Python version...")
    python_ok = check_python_version()
    print()
    
    print("Checking dependencies...")
    deps_ok = check_dependencies()
    print()
    
    print("Checking environment variables...")
    check_environment()
    print()
    
    print("=" * 50)
    if python_ok and deps_ok:
        print("✅ Setup validation PASSED!")
        print("You're ready to run: streamlit run pdf_chat_app.py")
    else:
        print("❌ Setup validation FAILED")
        print("Please install missing dependencies:")
        print("pip install -r requirements.txt")
    print("=" * 50)

if __name__ == "__main__":
    main()
