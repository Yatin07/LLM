"""
Text Processing Module
Handles text chunking, embedding, and vector storage for semantic search.
"""

import os
import logging
import pickle
from typing import List, Dict, Tuple, Optional
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss

logger = logging.getLogger(__name__)

class TextProcessor:
    """Process text for semantic search: chunking, embedding, and vector storage."""
    
    def __init__(self, 
                 model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200,
                 vector_store_path: str = "./vector_store"):
        """
        Initialize the text processor.
        
        Args:
            model_name: HuggingFace model name for embeddings
            chunk_size: Size of text chunks in characters
            chunk_overlap: Overlap between chunks in characters
            vector_store_path: Path to save/load vector store
        """
        self.model_name = model_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.vector_store_path = vector_store_path
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
        )
        
        # Initialize embedding model
        logger.info(f"Loading embedding model: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
        
        # Initialize vector store
        self.index = None
        self.documents = []  # Store chunk metadata
        self.load_or_create_index()
    
    def load_or_create_index(self):
        """Load existing FAISS index or create a new one."""
        index_path = os.path.join(self.vector_store_path, "faiss_index.bin")
        documents_path = os.path.join(self.vector_store_path, "documents.pkl")
        
        os.makedirs(self.vector_store_path, exist_ok=True)
        
        if os.path.exists(index_path) and os.path.exists(documents_path):
            try:
                # Load existing index
                self.index = faiss.read_index(index_path)
                with open(documents_path, 'rb') as f:
                    self.documents = pickle.load(f)
                logger.info(f"Loaded existing index with {len(self.documents)} documents")
            except Exception as e:
                logger.warning(f"Failed to load existing index: {e}")
                self._create_new_index()
        else:
            self._create_new_index()
    
    def _create_new_index(self):
        """Create a new FAISS index."""
        # Use IndexFlatIP for cosine similarity (inner product with normalized vectors)
        self.index = faiss.IndexFlatIP(self.embedding_dim)
        self.documents = []
        logger.info(f"Created new FAISS index with dimension {self.embedding_dim}")
    
    def save_index(self):
        """Save the FAISS index and document metadata."""
        try:
            index_path = os.path.join(self.vector_store_path, "faiss_index.bin")
            documents_path = os.path.join(self.vector_store_path, "documents.pkl")
            
            faiss.write_index(self.index, index_path)
            with open(documents_path, 'wb') as f:
                pickle.dump(self.documents, f)
            
            logger.info(f"Saved index with {len(self.documents)} documents")
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
            raise
    
    def chunk_text(self, text: str, source: str = "unknown") -> List[Dict]:
        """
        Split text into chunks with metadata.
        
        Args:
            text: Input text to chunk
            source: Source document identifier
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        try:
            # Ensure text is a string
            if not isinstance(text, str):
                logger.error(f"Text is not a string: {type(text)} - {text}")
                text = str(text)
            
            # Use a more robust text splitting approach
            try:
                chunks = self.text_splitter.split_text(text)
            except Exception as split_error:
                logger.warning(f"RecursiveCharacterTextSplitter failed: {split_error}")
                # Fallback to simple text splitting
                chunks = self._simple_text_split(text)
            
            chunk_docs = []
            for i, chunk in enumerate(chunks):
                if chunk.strip():  # Only add non-empty chunks
                    chunk_docs.append({
                        "text": chunk,
                        "source": source,
                        "chunk_id": i,
                        "chunk_size": len(chunk),
                        "total_chunks": len(chunks)
                    })
            
            logger.info(f"Created {len(chunk_docs)} chunks from {source}")
            return chunk_docs
            
        except Exception as e:
            logger.error(f"Error chunking text: {e}")
            logger.error(f"Text type: {type(text)}, Text preview: {str(text)[:100] if text else 'None'}")
            raise
    
    def _simple_text_split(self, text: str) -> List[str]:
        """Simple text splitting fallback method."""
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        chunks = []
        
        for paragraph in paragraphs:
            if len(paragraph.strip()) > 0:
                # If paragraph is too long, split by sentences
                if len(paragraph) > self.chunk_size:
                    sentences = paragraph.split('. ')
                    current_chunk = ""
                    
                    for sentence in sentences:
                        if len(current_chunk) + len(sentence) < self.chunk_size:
                            current_chunk += sentence + ". "
                        else:
                            if current_chunk.strip():
                                chunks.append(current_chunk.strip())
                            current_chunk = sentence + ". "
                    
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())
                else:
                    chunks.append(paragraph.strip())
        
        return chunks
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            NumPy array of embeddings
        """
        try:
            # Generate embeddings
            embeddings = self.embedding_model.encode(
                texts,
                show_progress_bar=len(texts) > 10,
                convert_to_numpy=True,
                normalize_embeddings=True  # Important for cosine similarity
            )
            
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def add_documents(self, text: str, source: str, metadata: Dict = None) -> int:
        """
        Add a document to the vector store.
        
        Args:
            text: Document text
            source: Source identifier
            metadata: Additional metadata
            
        Returns:
            Number of chunks added
        """
        try:
            # Chunk the text
            chunks = self.chunk_text(text, source)
            
            if not chunks:
                logger.warning(f"No chunks created for {source}")
                return 0
            
            # Extract texts for embedding
            chunk_texts = [chunk["text"] for chunk in chunks]
            
            # Generate embeddings
            embeddings = self.embed_texts(chunk_texts)
            
            # Add metadata to chunks
            for i, chunk in enumerate(chunks):
                chunk.update({
                    "doc_id": len(self.documents) + i,
                    "embedding_model": self.model_name,
                    "timestamp": os.path.getctime(os.path.abspath(__file__)) if os.path.exists(source) else None
                })
                if metadata:
                    chunk.update(metadata)
            
            # Add to FAISS index
            self.index.add(embeddings.astype(np.float32))
            
            # Store document metadata
            self.documents.extend(chunks)
            
            # Save the updated index
            self.save_index()
            
            logger.info(f"Added {len(chunks)} chunks from {source} to vector store")
            return len(chunks)
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise
    
    def search_similar(self, query: str, k: int = 5, score_threshold: float = 0.3) -> List[Dict]:
        """
        Search for similar documents using semantic similarity.
        
        Args:
            query: Search query
            k: Number of results to return
            score_threshold: Minimum similarity score threshold
            
        Returns:
            List of similar documents with scores
        """
        try:
            if len(self.documents) == 0:
                logger.warning("No documents in vector store")
                return []
            
            # Embed the query
            query_embedding = self.embed_texts([query])
            
            # Search in FAISS index
            scores, indices = self.index.search(query_embedding.astype(np.float32), k)
            
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx != -1 and score >= score_threshold:  # Valid index and above threshold
                    doc = self.documents[idx].copy()
                    doc["similarity_score"] = float(score)
                    results.append(doc)
            
            logger.info(f"Found {len(results)} similar documents for query")
            return results
            
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            raise
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector store."""
        total_docs = len(self.documents)
        sources = set(doc.get("source", "unknown") for doc in self.documents)
        
        avg_chunk_size = np.mean([doc.get("chunk_size", 0) for doc in self.documents]) if total_docs > 0 else 0
        
        return {
            "total_chunks": total_docs,
            "unique_sources": len(sources),
            "sources": list(sources),
            "average_chunk_size": int(avg_chunk_size),
            "embedding_model": self.model_name,
            "embedding_dimension": self.embedding_dim,
            "vector_store_path": self.vector_store_path
        }
    
    def clear_index(self):
        """Clear all documents from the vector store."""
        self._create_new_index()
        self.save_index()
        logger.info("Cleared vector store")

# Convenience functions
def create_text_processor(**kwargs) -> TextProcessor:
    """Create a text processor with default settings."""
    return TextProcessor(**kwargs)

def process_and_store_document(text: str, source: str, processor: Optional[TextProcessor] = None) -> Dict:
    """
    Process and store a document in one step.
    
    Args:
        text: Document text
        source: Source identifier
        processor: Optional TextProcessor instance
        
    Returns:
        Processing results
    """
    if processor is None:
        processor = create_text_processor()
    
    chunks_added = processor.add_documents(text, source)
    stats = processor.get_stats()
    
    return {
        "chunks_added": chunks_added,
        "total_chunks": stats["total_chunks"],
        "source": source,
        "status": "success"
    }