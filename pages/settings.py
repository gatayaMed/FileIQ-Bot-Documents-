"""
Settings page for FileIQ
"""

import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def render_settings():
    """Render settings page content"""
    st.title("⚙️ Settings")
    
    # LLM Configuration
    st.subheader("🤖 AI Model Configuration")
    
    # Provider selection
    provider = st.selectbox(
        "Select LLM Provider",
        options=["deepseek", "groq", "openai", "anthropic"],
        index=0,
        key="llm_provider_select"
    )
    
    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Lower = more focused, Higher = more creative"
    )
    
    # Display current API key status
    st.subheader("🔑 API Keys Status")
    
    api_key_status = {}
    
    # Check Deepseek
    has_deepseek = bool(load_dotenv('DEEPSEEK_API_KEY'))
    api_key_status['Deepseek'] = "✅ Set" if has_deepseek else "❌ Not set"
    
    # Check Groq
    has_groq = bool(load_dotenv('GROQ_API_KEY'))
    api_key_status['Groq'] = "✅ Set" if has_groq else "❌ Not set"
    
    # Check OpenAI
    has_openai = bool(load_dotenv('OPENAI_API_KEY'))
    api_key_status['OpenAI'] = "✅ Set" if has_openai else "❌ Not set"
    
    # Check Anthropic
    has_anthropic = bool(load_dotenv('ANTHROPIC_API_KEY'))
    api_key_status['Anthropic'] = "✅ Set" if has_anthropic else "❌ Not set"
    
    # Display status
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Providers:**")
        st.text(f"Deepseek: {api_key_status['Deepseek']}")
        st.text(f"Groq: {api_key_status['Groq']}")
    
    with col2:
        st.markdown("**Alternative LLMs:**")
        st.text(f"OpenAI: {api_key_status['OpenAI']}")
        st.text(f"Anthropic: {api_key_status['Anthropic']}")
    
    # Temporary API key input
    st.divider()
    st.subheader("🔑 Temporary API Key Input")
    st.warning("""
    Keys entered here are used ONLY for this session and will NOT be saved to .env file.
    For permanent keys, add them to your .env file on the server.
    """)
    
    temp_key_input = st.text_input(
        f"Enter {provider.upper()} API Key",
        type="password",
        help="This key is for this session only",
        key="temp_api_key_input"
    )
    
    if temp_key_input:
        import os
        provider_upper = provider.upper()
        os.environ[f"{provider_upper}_API_KEY"] = temp_key_input
        st.success(f"{provider.upper()} API key set for this session")
    
    # Clear session data
    st.divider()
    st.subheader("🗑️ Session Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear Chat History"):
            if 'chat_history' in st.session_state:
                st.session_state.chat_history = []
                st.success("Chat history cleared")
                st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Uploaded Documents"):
            if 'documents' in st.session_state:
                del st.session_state.documents
            if 'vectorstore' in st.session_state:
                del st.session_state.vectorstore
            st.success("Session data cleared")
            st.rerun()
    
    # App information
    st.divider()
    st.info("""
    📚 **Configuration Tips**
    
    - API keys should be added to `.env` file for persistence
    - Use temporary keys for testing without committing secrets
    - Vector store is recreated when new documents are uploaded
    - Chat history is stored in session and lost on page refresh
    """)


if __name__ == "__main__":
    render_settings()
