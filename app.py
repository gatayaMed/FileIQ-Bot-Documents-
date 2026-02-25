"""
FileIQ - Document Intelligence Bot
Advanced AI assistant for document Q&A with RAG, chat history, and multi-LLM support
"""

import streamlit as st
import os
import tempfile
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# LangChain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.callbacks import get_openai_callback
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Deepseek API
from deepseek import Chat

# Document processing
from pypdf import PdfReader
import pdfplumber
from docx import Document
from docx2txt import process as docx2txt

# LLM providers
import groq
from openai import OpenAI
import anthropic

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="FileIQ - Document Intelligence",
    page_icon="🤖",
    page_layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "pages/home.py": "Home",
        "pages/upload.py": "Upload Document",
        "pages/about.py": "About",
        "pages/settings.py": "Settings",
    }
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stMarkdown {
        color: #ffffff;
    }
    .chat-message {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .chat-user {
        background: #4a90e2;
        margin-right: auto;
    }
    .chat-ai {
        background: #00d4aa;
        margin-left: auto;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'llm_provider' not in st.session_state:
    st.session_state.llm_provider = 'deepseek'

if 'documents' not in st.session_state:
    st.session_state.documents = []

if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None


def get_llm(provider=None, model=None, temperature=0.7):
    """Initialize LLM based on provider selection"""
    provider = provider or st.session_state.llm_provider
    
    try:
        if provider == 'deepseek':
            if model:
                return Chat(model=model, temperature=temperature)
            return Chat(temperature=temperature)
        
        elif provider == 'groq':
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                st.error("Please add GROQ_API_KEY in settings")
                return None
            return groq.ChatGroq(api_key=api_key, model=model or 'llama-3-70b-instruct', temperature=temperature)
        
        elif provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                st.error("Please add OPENAI_API_KEY in settings")
                return None
            return OpenAI(api_key=api_key, model=model or 'gpt-4o', temperature=temperature)
        
        elif provider == 'anthropic':
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                st.error("Please add ANTHROPIC_API_KEY in settings")
                return None
            return anthropic.Anthropic(api_key=api_key, model=model or 'claude-3-opus-20240229', temperature=temperature)
        
        else:
            st.error(f"Unknown provider: {provider}")
            return None
            
    except Exception as e:
        st.error(f"Error initializing LLM: {str(e)}")
        return None


def process_document(file_path):
    """Process uploaded document and extract text"""
    file_path = str(file_path)
    file_ext = Path(file_path).suffix.lower()
    
    try:
        # PDF processing
        if file_ext == '.pdf':
            try:
                reader = PdfReader(file_path)
                text = "\n".join([page.extract_text() for page in reader.pages])
                return text, file_ext
            except Exception:
                # Fallback to pdfplumber
                with open(file_path, 'rb') as f:
                    pdf = pdfplumber.PDF(f)
                    text = "\n".join([page.extract_text() for page in pdf.pages])
                return text, file_ext
        
        # DOCX processing
        elif file_ext == '.docx':
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text, file_ext
        
        # TXT processing
        elif file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return text, file_ext
        
        else:
            return None, file_ext
            
    except Exception as e:
        st.error(f"Error processing document: {str(e)}")
        return None, None


def create_vectorstore(documents):
    """Create FAISS vector store from documents"""
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        texts = []
        metadatas = []
        for i, (doc_text, doc_ext) in enumerate(documents):
            chunks = text_splitter.split_text(doc_text)
            texts.extend(chunks)
            metadatas.extend([{
                "source": f"document_{i}",
                "type": doc_ext,
                "chunk_id": j,
            } for j in range(len(chunks))])
        
        # Create FAISS index
        vectorstore = FAISS.from_texts(
            texts=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
        return vectorstore
        
    except Exception as e:
        st.error(f"Error creating vector store: {str(e)}")
        return None


def render_chat_interface():
    """Render main chat interface"""
    st.title("🤖 FileIQ - Document Intelligence")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # LLM Provider Selection
        st.subheader("🤖 AI Model")
        provider = st.selectbox(
            "Select LLM Provider",
            options=["deepseek", "groq", "openai", "anthropic"],
            index=0,
            key="llm_provider_select"
        )
        st.session_state.llm_provider = provider
        
        # Model selection based on provider
        if provider == "deepseek":
            model = st.selectbox(
                "Model",
                options=["deepseek-chat", "deepseek-coder"],
                index=0
            )
        elif provider == "groq":
            model = st.selectbox(
                "Model",
                options=["llama-3-70b-instruct", "mixtral-8x7b-instruct"],
                index=0
            )
        elif provider == "openai":
            model = st.selectbox(
                "Model",
                options=["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
                index=0
            )
        elif provider == "anthropic":
            model = st.selectbox(
                "Model",
                options=["claude-3-opus-20240229", "claude-3-5-sonnet-20240220"],
                index=0
            )
        
        # Temperature slider
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1
        )
        
        # API Keys display
        st.subheader("🔑 API Keys")
        api_key_status = {}
        
        if provider == 'groq':
            has_key = bool(os.getenv('GROQ_API_KEY'))
            api_key_status['Groq'] = "✅ Set" if has_key else "❌ Not set"
            if not has_key:
                st.warning("Add GROQ_API_KEY in .env or use the key input below")
        
        if provider == 'openai':
            has_key = bool(os.getenv('OPENAI_API_KEY'))
            api_key_status['OpenAI'] = "✅ Set" if has_key else "❌ Not set"
            if not has_key:
                st.warning("Add OPENAI_API_KEY in .env or use the key input below")
        
        if provider == 'anthropic':
            has_key = bool(os.getenv('ANTHROPIC_API_KEY'))
            api_key_status['Anthropic'] = "✅ Set" if has_key else "❌ Not set"
            if not has_key:
                st.warning("Add ANTHROPIC_API_KEY in .env or use the key input below")
        
        # Display status
        for key, status in api_key_status.items():
            st.text(f"{key}: {status}")
        
        # Temporary API key input
        st.subheader("Temporary Key Input")
        temp_key = st.text_input(
            f"Enter {provider.upper()} API Key",
            type="password",
            help="This key is used only for this session and won't be saved"
        )
        if temp_key:
            os.environ[f"{provider.upper()}_API_KEY"] = temp_key
            st.success(f"{provider.upper()} API key set for this session")
        
        # Clear chat history
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
        
        # Export chat
        if st.button("📥 Export Chat"):
            if st.session_state.chat_history:
                chat_text = "\n\n".join([
                    f"{'You' if msg['role'] == 'user' else 'AI'}: {msg['content']}"
                    for msg in st.session_state.chat_history
                ])
                st.download_button(
                    label="Download Chat History",
                    data=chat_text,
                    file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
    
    # Main content area
    st.header("💬 Chat with Documents")
    
    # Document upload section
    with st.expander("📄 Upload Documents", expanded=True):
        uploaded_files = st.file_uploader(
            "Upload PDF, DOCX, or TXT files",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            help="Supported formats: PDF, DOCX, TXT"
        )
        
        if uploaded_files:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📚 Process Documents", use_container_width=True):
                    with st.spinner("Processing documents..."):
                        new_documents = []
                        for uploaded_file in uploaded_files:
                            # Save to temp file
                            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
                                tmp.write(uploaded_file.getbuffer())
                                tmp_path = tmp.name
                            
                            # Process document
                            text, doc_type = process_document(tmp_path)
                            
                            if text:
                                new_documents.append({
                                    'text': text,
                                    'type': doc_type,
                                    'name': uploaded_file.name
                                })
                                st.success(f"✅ Processed: {uploaded_file.name}")
                            
                            # Cleanup temp file
                            os.unlink(tmp_path)
                        
                        if new_documents:
                            st.session_state.documents.extend(new_documents)
                            
                            # Update vector store
                            if st.button("🔍 Create Search Index", key="create_index_btn"):
                                with st.spinner("Creating vector store..."):
                                    st.session_state.vectorstore = create_vectorstore(
                                        [doc['text'] for doc in st.session_state.documents]
                                    )
                                    if st.session_state.vectorstore:
                                        st.success(f"✅ Created index for {len(st.session_state.documents)} documents")
            
            with col2:
                st.info(f"""
                📊 **Uploaded Documents:** {len(st.session_state.documents)}
                
                📋 **Supported Formats:**
                - PDF (.pdf)
                - Word (.docx)
                - Text (.txt)
                
                🔍 **Search:** Documents are indexed for RAG retrieval
                """)
    
    # Document comparison section
    with st.expander("📄 Document Comparison", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            doc1 = st.file_uploader("Document 1", type=['pdf', 'docx', 'txt'], key='doc1')
        
        with col2:
            doc2 = st.file_uploader("Document 2", type=['pdf', 'docx', 'txt'], key='doc2')
        
        if st.button("🔍 Compare Documents", key='compare_btn'):
            if doc1 and doc2:
                with st.spinner("Comparing documents..."):
                    text1, type1 = process_document(doc1)
                    text2, type2 = process_document(doc2)
                    
                    if text1 and text2:
                        st.subheader("Comparison Results")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Doc 1", f"{len(text1)} chars")
                        
                        with col2:
                            st.metric("Doc 2", f"{len(text2)} chars")
                        
                        with col3:
                            similarity = len(set(text1.split()) & set(text2.split())) / len(set(text1.split()) | set(text2.split()))
                            st.metric("Similarity", f"{similarity*100:.1f}%")
                        
                        st.markdown("### Content Comparison")
                        
                        # Show key differences
                        words1 = set(text1.lower().split())
                        words2 = set(text2.lower().split())
                        
                        unique_to_doc1 = words1 - words2
                        unique_to_doc2 = words2 - words1
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Unique to Doc 1:** {len(unique_to_doc1)} words")
                        with col2:
                            st.markdown(f"**Unique to Doc 2:** {len(unique_to_doc2)} words")
                        
                        st.markdown("#### Text Preview")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.text_area("Doc 1 Content", text1[:1000] + "...", height=200, key='preview1')
                        with col2:
                            st.text_area("Doc 2 Content", text2[:1000] + "...", height=200, key='preview2')
    
    # Chat interface
    st.divider()
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.chat_message(message['content'], avatar="👤")
        else:
            # Add citation if available
            content = message['content']
            if 'source' in message and 'source_type' in message:
                citation = f"\n\n📄 *Source: {message['source']} ({message['source_type']})*"
                content += citation
            
            st.chat_message(content, avatar="🤖")
    
    # Chat input
    with st.form(key="chat_form"):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "Ask your documents...",
                placeholder="Type your question here...",
                key="user_input"
            )
        
        with col2:
            use_rag = st.checkbox("🔍 Use RAG", value=True, key='use_rag_cb',
                            help="Use retrieved documents for context")
        
        submitted = st.form_submit_button("Send 📤", use_container_width=True)
    
    if submitted and user_input:
        # Initialize LLM
        llm = get_llm(temperature=temperature)
        
        if not llm:
            st.error("Failed to initialize LLM. Please check your settings.")
            return
        
        # RAG context
        context_docs = []
        if use_rag and st.session_state.vectorstore:
            retriever = st.session_state.vectorstore.as_retriever(
                search_kwargs={"k": 3}
            )
            relevant_docs = retriever.get_relevant_documents(user_input)
            
            if relevant_docs:
                context_docs = [doc.page_content for doc in relevant_docs]
                st.info(f"🔍 Found {len(context_docs)} relevant document chunks")
        
        # Create conversation chain
        if context_docs:
            system_message = SystemMessage(
                content="You are a helpful AI assistant. Answer questions based on the provided context from uploaded documents. If the answer is not in the context, say so. Always cite your sources."
            )
            
            chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=st.session_state.vectorstore.as_retriever(search_kwargs={"k": 3}),
                memory=ConversationBufferMemory(
                    memory_key=f"{provider}_chat",
                    return_messages=True
                )
        else:
            system_message = SystemMessage(
                content="You are a helpful AI assistant. Answer the user's questions helpfully."
            )
            
            from langchain.chains import ConversationChain
            chain = ConversationChain(
                llm=llm,
                memory=ConversationBufferMemory(
                    memory_key=f"{provider}_chat",
                    return_messages=True
                )
            )
        
        # Generate response
        with st.spinner("Thinking..."):
            try:
                if context_docs:
                    response = chain.invoke({"question": user_input})
                    ai_response = response['answer']
                    sources = [doc.metadata for doc in context_docs[:3]] if context_docs else []
                else:
                    response = chain.invoke({"input": user_input})
                    ai_response = response['response']
                    sources = []
                
                # Add to chat history
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_input,
                    'timestamp': datetime.now().isoformat()
                })
                
                ai_message = {
                    'role': 'ai',
                    'content': ai_response,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Add source information if available
                if sources:
                    ai_message['source'] = sources[0]['source'] if sources else "unknown"
                    ai_message['source_type'] = sources[0]['type'] if sources else "unknown"
                
                st.session_state.chat_history.append(ai_message)
                st.rerun()
                
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")


def main():
    """Main application entry point"""
    render_chat_interface()


if __name__ == "__main__":
    main()
