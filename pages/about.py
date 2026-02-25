"""
About page for FileIQ
"""

import streamlit as st


def render_about():
    """Render about page content"""
    st.title("ℹ️ About FileIQ")
    
    st.markdown("""
    # 🤖 What is FileIQ?
    
    FileIQ is an advanced AI-powered document intelligence platform designed to help users interact with their documents in natural language.
    
    ---
    
    ## 🎯 Mission
    
    To make document analysis and information retrieval as intuitive as asking a colleague.
    
    ---
    
    ## ✨ Key Features
    
    ### 📄 Document Processing
    - Support for PDF, DOCX, and TXT files
    - Fast and accurate text extraction
    - Automatic chunking for better AI understanding
    
    ### 🤖 Multi-LLM Support
    - **Deepseek** (Primary): Advanced open-source LLM
    - **Groq** (Alternative): Fast, efficient inference
    - **OpenAI** (Alternative): Industry-leading models
    - **Anthropic** (Alternative): Advanced reasoning capabilities
    
    ### 🔍 RAG-Powered Retrieval
    - Semantic search across uploaded documents
    - FAISS vector store for fast similarity matching
    - Source citations for AI answers
    
    ### 💬 Conversational Interface
    - Maintains conversation history
    - Context-aware responses
    - Export chat history
    
    ---
    
    ## 🛠️ Technology Stack
    
    - **Streamlit**: Modern web interface
    - **LangChain**: LLM orchestration
    - **FAISS**: Vector similarity search
    - **HuggingFace**: Text embeddings
    - **Pypdf/pdfplumber**: Document processing
    
    ---
    
    ## 📊 Use Cases
    
    - **Tradespeople**: Analyze contracts, manuals, and technical documents
    - **Students**: Study lecture notes and textbooks
    - **Researchers**: Search across multiple papers and reports
    - **Business**: Compare quotes, analyze legal documents
    
    ---
    
    ## 🤝 Built With
    
    - ❤️ for tradespeople and everyday users
    - 🇩🇪 German and English support
    - 🌐 Fully responsive design
    - 🔒 Security-first approach
    
    ---
    
    ## 📄 Support
    
    For issues, questions, or suggestions:
    
    - 📧 Create an issue on [GitHub](https://github.com/gatayaMed/FileIQ-Bot-Documents-/issues)
    - 📧 Email: med@smarta.website
    - 📧 Visit: [smarta.website](https://smarta.website)
    
    ---
    
    *Version 1.0.0 - 2026*
    """)


if __name__ == "__main__":
    render_about()
