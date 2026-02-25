"""
Document upload page for FileIQ
"""

import streamlit as st
from utils.document_loader import process_document
from utils.vector_store import create_vectorstore


def render_upload():
    """Render document upload interface"""
    st.title("📄 Upload Documents")
    st.markdown("Upload PDF, DOCX, or TXT files for AI analysis")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose files",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        help="Supported formats: PDF, DOCX, TXT",
        label="Select files to upload"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) selected")
        
        # Display file info
        with st.expander("📋 File Details", expanded=True):
            for i, uploaded_file in enumerate(uploaded_files):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**{i+1}. {uploaded_file.name}**")
                    st.code(f"Size: {uploaded_file.size / 1024:.2f} KB")
                
                with col2:
                    file_type = uploaded_file.name.split('.')[-1].upper()
                    st.write(f"Type: {file_type}")
        
        # Process documents
        if st.button("📚 Process Documents", use_container_width=True):
            with st.spinner("Processing documents..."):
                new_documents = []
                
                for uploaded_file in uploaded_files:
                    # Save to temp file
                    import tempfile
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
                    import os
                    os.unlink(tmp_path)
                
                if new_documents:
                    # Add to session state
                    if 'documents' not in st.session_state:
                        st.session_state.documents = []
                    
                    st.session_state.documents.extend(new_documents)
                    st.info(f"✅ {len(new_documents)} document(s) processed and added to library")
                    
                    # Create vector store
                    if st.button("🔍 Create Search Index", key="create_index_btn"):
                        with st.spinner("Creating vector store..."):
                            vectorstore = create_vectorstore(
                                [doc['text'] for doc in st.session_state.documents]
                            )
                            
                            if vectorstore:
                                st.session_state.vectorstore = vectorstore
                                st.success(f"✅ Created index for {len(st.session_state.documents)} documents")
                            else:
                                st.error("❌ Failed to create vector store")
                else:
                    st.error("❌ No documents to process")


if __name__ == "__main__":
    render_upload()
