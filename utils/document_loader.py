"""
Document loader utility for FileIQ
"""

import tempfile
import os
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None
    print("Warning: pypdf not installed, using fallback")

try:
    import pdfplumber
except ImportError:
    pdfplumber = None
    print("Warning: pdfplumber not installed, using fallback")

from docx import Document
from docx2txt import process as docx2txt


def process_document(file_path):
    """Process uploaded document and extract text"""
    file_path = str(file_path)
    file_ext = Path(file_path).suffix.lower()
    
    try:
        # PDF processing
        if file_ext == '.pdf':
            return process_pdf(file_path), file_ext
        
        # DOCX processing
        elif file_ext == '.docx':
            return process_docx(file_path), file_ext
        
        # TXT processing
        elif file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return text, file_ext
        
        else:
            return None, file_ext
            
    except Exception as e:
        print(f"Error processing document: {str(e)}")
        return None, file_ext


def process_pdf(file_path):
    """Process PDF document and extract text"""
    text = ""
    
    # Try pypdf first
    if PdfReader:
        try:
            reader = PdfReader(file_path)
            text = "\n".join([page.extract_text() for page in reader.pages])
            return text
        except Exception as e:
            print(f"pypdf error: {e}, trying pdfplumber")
    
    # Fallback to pdfplumber
    if pdfplumber:
        try:
            pdf = pdfplumber.PDF(file_path)
            text = "\n".join([page.extract_text() for page in pdf.pages])
            return text
        except Exception as e:
            print(f"pdfplumber error: {e}")
    
    return text


def process_docx(file_path):
    """Process DOCX document and extract text"""
    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error processing DOCX: {e}")
        return ""
