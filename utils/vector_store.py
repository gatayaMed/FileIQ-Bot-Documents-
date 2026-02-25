"""
Vector store utility for FileIQ using FAISS
"""

import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.messages import Document as LangchainDocument

load_dotenv()


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
        
        for i, (doc_text, doc_type) in enumerate(documents):
            chunks = text_splitter.split_text(doc_text)
            texts.extend(chunks)
            metadatas.extend([{
                "source": f"document_{i}",
                "type": doc_type,
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


def search_documents(vectorstore, query, k=3):
    """Search documents using vector store"""
    if not vectorstore:
        return []
    
    try:
        retriever = vectorstore.as_retriever(search_kwargs={"k": k})
        relevant_docs = retriever.get_relevant_documents(query)
        return relevant_docs
    except Exception as e:
        st.error(f"Error searching documents: {str(e)}")
        return []
