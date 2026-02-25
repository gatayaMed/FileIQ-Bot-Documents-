"""
API configuration utility for FileIQ
"""

from dotenv import load_dotenv

load_dotenv()


# Configuration
class Config:
    """Application configuration"""
    
    # LLM Providers
    PROVIDERS = {
        'deepseek': 'Deepseek (Primary)',
        'groq': 'Groq',
        'openai': 'OpenAI',
        'anthropic': 'Anthropic Claude'
    }
    
    # Default Settings
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_TOP_K = 3
    MAX_DOCUMENTS = 10
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200


def get_api_key(provider_name):
    """Get API key from environment or session"""
    provider_upper = provider_name.upper()
    
    # Check session state first
    import streamlit as st
    temp_key = st.session_state.get(f"{provider_upper}_API_KEY", None)
    if temp_key:
        return temp_key
    
    # Fallback to .env
    import os
    return os.getenv(f"{provider_upper}_API_KEY", None)


def set_temp_api_key(provider_name, key):
    """Set temporary API key in session"""
    import streamlit as st
    provider_upper = provider_name.upper()
    st.session_state[f"{provider_upper}_API_KEY"] = key
