"""
AI handler utility for FileIQ
"""

from dotenv import load_dotenv
from deepseek import Chat as DeepseekChat
from groq import ChatGroq
from openai import OpenAI
from anthropic import Anthropic

load_dotenv()


def get_llm(provider=None, model=None, temperature=0.7):
    """Initialize LLM based on provider selection"""
    
    provider = provider or load_dotenv('LLM_PROVIDER', 'deepseek')
    
    try:
        if provider == 'deepseek':
            if model:
                return DeepseekChat(model=model, temperature=temperature)
            return DeepseekChat(temperature=temperature)
        
        elif provider == 'groq':
            api_key = load_dotenv('GROQ_API_KEY')
            if not api_key:
                raise ValueError("Please add GROQ_API_KEY in settings or enter temporary key")
            model = model or 'llama-3-70b-instruct'
            return ChatGroq(api_key=api_key, model=model, temperature=temperature)
        
        elif provider == 'openai':
            api_key = load_dotenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("Please add OPENAI_API_KEY in settings or enter temporary key")
            model = model or 'gpt-4o'
            return OpenAI(api_key=api_key, model=model, temperature=temperature)
        
        elif provider == 'anthropic':
            api_key = load_dotenv('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError("Please add ANTHROPIC_API_KEY in settings or enter temporary key")
            model = model or 'claude-3-opus-20240229'
            return Anthropic(api_key=api_key, model=model, temperature=temperature)
        
        else:
            raise ValueError(f"Unknown provider: {provider}")
            
    except Exception as e:
        # Return error message that can be displayed
        return None
