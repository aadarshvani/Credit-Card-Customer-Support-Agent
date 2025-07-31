#!/usr/bin/env python3
"""
Test script for AmEx AI Credit Support Agent
This script tests all major components to ensure they work correctly.
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit
        print("✅ streamlit")
    except ImportError as e:
        print(f"❌ streamlit: {e}")
        return False
    
    try:
        from langgraph.graph import StateGraph, END
        print("✅ langgraph")
    except ImportError as e:
        print(f"❌ langgraph: {e}")
        return False
    
    try:
        from langchain_groq import ChatGroq
        print("✅ langchain-groq")
    except ImportError as e:
        print(f"❌ langchain-groq: {e}")
        return False
    
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
        print("✅ langchain-huggingface")
    except ImportError as e:
        print(f"❌ langchain-huggingface: {e}")
        return False
    
    try:
        import faiss
        print("✅ faiss")
    except ImportError as e:
        print(f"❌ faiss: {e}")
        return False
    
    return True

def test_core_modules():
    """Test core modules"""
    print("\nTesting core modules...")
    
    try:
        from core.config import GROQ_API_KEY
        print("✅ core.config")
    except Exception as e:
        print(f"❌ core.config: {e}")
        return False
    
    try:
        from core.llm import get_llm
        print("✅ core.llm")
    except Exception as e:
        print(f"❌ core.llm: {e}")
        return False
    
    try:
        from core.embeddings import get_embeddings
        print("✅ core.embeddings")
    except Exception as e:
        print(f"❌ core.embeddings: {e}")
        return False
    
    return True

def test_agents():
    """Test agent modules"""
    print("\nTesting agents...")
    
    try:
        from agents.router import route_query
        print("✅ agents.router")
    except Exception as e:
        print(f"❌ agents.router: {e}")
        return False
    
    try:
        from agents.aggregator import aggregate_responses
        print("✅ agents.aggregator")
    except Exception as e:
        print(f"❌ agents.aggregator: {e}")
        return False
    
    try:
        from agents.quality_checker import check_response_quality
        print("✅ agents.quality_checker")
    except Exception as e:
        print(f"❌ agents.quality_checker: {e}")
        return False
    
    return True

def test_tools():
    """Test tool modules"""
    print("\nTesting tools...")
    
    try:
        from tools.churn import predict_churn
        print("✅ tools.churn")
    except Exception as e:
        print(f"❌ tools.churn: {e}")
        return False
    
    try:
        from tools.credit import check_credit_approval
        print("✅ tools.credit")
    except Exception as e:
        print(f"❌ tools.credit: {e}")
        return False
    
    try:
        from tools.web_search import search_web
        print("✅ tools.web_search")
    except Exception as e:
        print(f"❌ tools.web_search: {e}")
        return False
    
    try:
        from tools.human_review import request_human_review
        print("✅ tools.human_review")
    except Exception as e:
        print(f"❌ tools.human_review: {e}")
        return False
    
    return True

def test_rag():
    """Test RAG modules"""
    print("\nTesting RAG modules...")
    
    try:
        from rag.rag_engine import query_knowledge_base
        print("✅ rag.rag_engine")
    except Exception as e:
        print(f"❌ rag.rag_engine: {e}")
        return False
    
    try:
        from rag.vector_store import build_faiss_index, search_faiss
        print("✅ rag.vector_store")
    except Exception as e:
        print(f"❌ rag.vector_store: {e}")
        return False
    
    try:
        from rag.text_splitter import split_markdown
        print("✅ rag.text_splitter")
    except Exception as e:
        print(f"❌ rag.text_splitter: {e}")
        return False
    
    return True

def test_manager():
    """Test manager modules"""
    print("\nTesting manager modules...")
    
    try:
        from manager.state import SessionState
        print("✅ manager.state")
    except Exception as e:
        print(f"❌ manager.state: {e}")
        return False
    
    try:
        from manager.prompts import INTENT_CLASSIFICATION_PROMPT
        print("✅ manager.prompts")
    except Exception as e:
        print(f"❌ manager.prompts: {e}")
        return False
    
    return True

def test_app():
    """Test main app modules"""
    print("\nTesting app modules...")
    
    try:
        from app import app_flow
        print("✅ app (LangGraph flow)")
    except Exception as e:
        print(f"❌ app: {e}")
        return False
    
    try:
        from main import add_message
        print("✅ main (Streamlit app)")
    except Exception as e:
        print(f"❌ main: {e}")
        return False
    
    return True

def test_environment():
    """Test environment variables"""
    print("\nTesting environment variables...")
    
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and groq_key != "your_groq_api_key_here":
        print("✅ GROQ_API_KEY is set")
    else:
        print("⚠️  GROQ_API_KEY not set (required for LLM functionality)")
    
    web_search_key = os.getenv("WEB_SEARCH_API_KEY")
    if web_search_key and web_search_key != "your_search_api_key_here":
        print("✅ WEB_SEARCH_API_KEY is set")
    else:
        print("⚠️  WEB_SEARCH_API_KEY not set (web search will be simulated)")
    
    return True

def main():
    """Run all tests"""
    print("🏦 AmEx AI Credit Support Agent - Component Test")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_core_modules,
        test_agents,
        test_tools,
        test_rag,
        test_manager,
        test_app,
        test_environment
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print(f"❌ Test failed: {test.__name__}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("streamlit run main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Set up environment variables in .env file")
        print("3. Run setup script: python setup.py")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 