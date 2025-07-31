#!/usr/bin/env python3
"""
Setup script for AmEx AI Credit Support Agent
This script helps initialize the project and build the FAISS index.
"""

import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit', 'langchain', 'langchain-groq', 'langchain-huggingface',
        'langgraph', 'chromadb', 'faiss-cpu', 'sentence-transformers'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nPlease install missing packages with:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_env_vars():
    """Check if required environment variables are set"""
    required_vars = ['GROQ_API_KEY']
    optional_vars = ['WEB_SEARCH_API_KEY', 'CHURN_MODEL_API', 'CREDIT_MODEL_API']
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    if missing_required:
        print("❌ Missing required environment variables:")
        for var in missing_required:
            print(f"   - {var}")
        print("\nPlease set these environment variables in your .env file")
        return False
    
    if missing_optional:
        print("⚠️  Missing optional environment variables (features will be limited):")
        for var in missing_optional:
            print(f"   - {var}")
    
    print("✅ Environment variables configured")
    return True

def build_faiss_index():
    """Build FAISS index from knowledge base"""
    try:
        from rag.vector_store import build_faiss_index
        
        knowledge_base_path = "rag/knowledge_base/faqs.md"
        if not os.path.exists(knowledge_base_path):
            print(f"❌ Knowledge base file not found: {knowledge_base_path}")
            return False
        
        print("🔍 Building FAISS index...")
        build_faiss_index(knowledge_base_path)
        print("✅ FAISS index built successfully")
        return True
    except Exception as e:
        print(f"❌ Error building FAISS index: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("🏦 AmEx AI Credit Support Agent - Setup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment variables
    if not check_env_vars():
        sys.exit(1)
    
    # Build FAISS index
    if not build_faiss_index():
        print("\n⚠️  FAISS index build failed. You can still run the app, but RAG features will be limited.")
    
    print("\n✅ Setup completed successfully!")
    print("\nTo run the application:")
    print("streamlit run main.py")
    
    print("\nTo run the LangGraph flow directly:")
    print("python app.py")

if __name__ == "__main__":
    main() 