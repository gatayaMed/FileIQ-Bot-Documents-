"""
Home page for FileIQ application
"""

import streamlit as st
from utils.ai_handler import get_llm
from utils.vector_store import create_vectorstore


def render_home():
    """Render home page content"""
    st.title("🤖 FileIQ - Document Intelligence")
    
    # Hero section
    st.markdown("""
    # 🤖 Welcome to FileIQ
    
    Transform your documents into actionable insights with AI-powered analysis.
    
    [📄 Upload Documents](#upload) | [🔧 Document Comparison](#comparison)
    """)
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📄 Documents", "0", help="Uploaded documents")
    
    with col2:
        st.metric("🔍 Search Index", "Not created", help="Vector store status")
    
    with col3:
        st.metric("💬 Chat Messages", "0", help="Conversation count")
    
    st.divider()
    
    # Features showcase
    st.subheader("✨ Features")
    
    feature_cols = st.columns(3)
    
    with feature_cols[0]:
        st.markdown("""
        ### 📄 Document Upload
        
        Upload PDF, DOCX, and TXT files for instant analysis.
        
        • Multiple file support
        • Automatic text extraction
        • Fast processing
        """)
    
    with feature_cols[1]:
        st.markdown("""
        ### 🤖 AI Chat
        
        Interact with your documents using natural language.
        
        • Multi-LLM support
        • RAG-enabled retrieval
        • Conversation history
        """)
    
    with feature_cols[2]:
        st.markdown("""
        ### 📊 Document Comparison
        
        Compare documents side-by-side with detailed analysis.
        
        • Similarity scoring
        • Unique word analysis
        • Content preview
        """)
    
    st.divider()
    
    # CTA section
    st.info("""
    🚀 **Get Started**
    
    Upload your first document to begin exploring the AI-powered features!
    
    Use the **Upload Documents** button in the sidebar or navigate to other pages.
    """)


if __name__ == "__main__":
    render_home()
