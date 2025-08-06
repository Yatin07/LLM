"""
Document Processing Module
Handles text extraction from various document formats (PDF, DOCX, TXT).
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
import fitz  # PyMuPDF
import pdfplumber
from PyPDF2 import PdfReader
from pathlib import Path

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Process and extract text from various document formats."""
    
    def __init__(self):
        self.supported_formats = {'.pdf', '.txt', '.docx'}
    
    def extract_text_from_file(self, filepath: str) -> Dict[str, any]:
        """
        Extract text from a file based on its format.
        
        Args:
            filepath: Path to the document file
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        file_extension = Path(filepath).suffix.lower()
        
        if file_extension == '.pdf':
            return self._extract_from_pdf(filepath)
        elif file_extension == '.txt':
            return self._extract_from_txt(filepath)
        elif file_extension == '.docx':
            return self._extract_from_docx(filepath)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def _extract_from_pdf(self, filepath: str) -> Dict[str, any]:
        """
        Extract text from PDF using multiple methods for robustness.
        Tries PyMuPDF first, falls back to pdfplumber, then PyPDF2.
        """
        text_content = ""
        metadata = {"pages": 0, "method": "", "file_size": os.path.getsize(filepath)}
        
        # Method 1: PyMuPDF (fastest and most reliable)
        try:
            doc = fitz.open(filepath)
            pages_text = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                page_text = page.get_text()
                if page_text.strip():  # Only add non-empty pages
                    pages_text.append(f"--- Page {page_num + 1} ---\n{page_text}")
            
            text_content = "\n\n".join(pages_text)
            metadata["pages"] = len(doc)
            metadata["method"] = "PyMuPDF"
            doc.close()
            
            if text_content.strip():
                logger.info(f"Successfully extracted text using PyMuPDF: {len(text_content)} characters")
                return {"text": text_content, "metadata": metadata}
                
        except Exception as e:
            logger.warning(f"PyMuPDF extraction failed: {str(e)}")
        
        # Method 2: pdfplumber (better for complex layouts)
        try:
            with pdfplumber.open(filepath) as pdf:
                pages_text = []
                
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        pages_text.append(f"--- Page {page_num + 1} ---\n{page_text}")
                
                text_content = "\n\n".join(pages_text)
                metadata["pages"] = len(pdf.pages)
                metadata["method"] = "pdfplumber"
                
                if text_content.strip():
                    logger.info(f"Successfully extracted text using pdfplumber: {len(text_content)} characters")
                    return {"text": text_content, "metadata": metadata}
                    
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed: {str(e)}")
        
        # Method 3: PyPDF2 (fallback)
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PdfReader(file)
                pages_text = []
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        pages_text.append(f"--- Page {page_num + 1} ---\n{page_text}")
                
                text_content = "\n\n".join(pages_text)
                metadata["pages"] = len(pdf_reader.pages)
                metadata["method"] = "PyPDF2"
                
                if text_content.strip():
                    logger.info(f"Successfully extracted text using PyPDF2: {len(text_content)} characters")
                    return {"text": text_content, "metadata": metadata}
                    
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {str(e)}")
        
        # If all methods fail
        raise Exception("Failed to extract text from PDF using all available methods")
    
    def _extract_from_txt(self, filepath: str) -> Dict[str, any]:
        """Extract text from plain text file."""
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    with open(filepath, 'r', encoding=encoding) as file:
                        text_content = file.read()
                        
                    metadata = {
                        "pages": 1,
                        "method": f"plain_text_{encoding}",
                        "file_size": os.path.getsize(filepath),
                        "encoding": encoding
                    }
                    
                    logger.info(f"Successfully extracted text from TXT file: {len(text_content)} characters")
                    return {"text": text_content, "metadata": metadata}
                    
                except UnicodeDecodeError:
                    continue
            
            raise Exception("Failed to read text file with any supported encoding")
            
        except Exception as e:
            logger.error(f"Text file extraction failed: {str(e)}")
            raise
    
    def _extract_from_docx(self, filepath: str) -> Dict[str, any]:
        """Extract text from Word document."""
        try:
            # Import here to avoid dependency issues if python-docx not installed
            from docx import Document
            
            doc = Document(filepath)
            paragraphs = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    paragraphs.append(paragraph.text)
            
            text_content = "\n\n".join(paragraphs)
            
            metadata = {
                "pages": 1,  # DOCX doesn't have clear page breaks
                "method": "python-docx",
                "file_size": os.path.getsize(filepath),
                "paragraphs": len(paragraphs)
            }
            
            logger.info(f"Successfully extracted text from DOCX file: {len(text_content)} characters")
            return {"text": text_content, "metadata": metadata}
            
        except ImportError:
            logger.error("python-docx not installed. Add 'python-docx' to requirements.txt")
            raise Exception("DOCX processing not available - missing python-docx dependency")
        except Exception as e:
            logger.error(f"DOCX extraction failed: {str(e)}")
            raise
    
    def validate_extracted_text(self, text: str, min_length: int = 50) -> bool:
        """
        Validate that extracted text is meaningful.
        
        Args:
            text: Extracted text content
            min_length: Minimum character length for valid text
            
        Returns:
            True if text appears valid, False otherwise
        """
        if not text or len(text.strip()) < min_length:
            return False
        
        # Check if text is mostly readable (not just special characters)
        readable_chars = sum(1 for c in text if c.isalnum() or c.isspace())
        if readable_chars < len(text) * 0.7:  # At least 70% readable characters
            return False
        
        return True
    
    def get_document_stats(self, text: str) -> Dict[str, int]:
        """Get basic statistics about the extracted text."""
        lines = text.split('\n')
        words = text.split()
        
        return {
            "characters": len(text),
            "words": len(words),
            "lines": len(lines),
            "non_empty_lines": len([line for line in lines if line.strip()]),
            "estimated_pages": max(1, len(words) // 250)  # Rough estimate: 250 words per page
        }

# Convenience function for simple usage
def extract_text_from_document(filepath: str) -> Tuple[str, Dict]:
    """
    Simple function to extract text from a document.
    
    Args:
        filepath: Path to the document
        
    Returns:
        Tuple of (extracted_text, metadata)
    """
    processor = DocumentProcessor()
    result = processor.extract_text_from_file(filepath)
    return result["text"], result["metadata"]