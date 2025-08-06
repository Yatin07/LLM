"""
LLM Document Processing System
Main Flask application for processing natural language queries against unstructured documents.
"""

import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from document_processor import DocumentProcessor, extract_text_from_document
from text_processor import TextProcessor, create_text_processor
from llm_processor import LLMProcessor, create_llm_processor, get_recommended_model

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Enable CORS for all routes
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
API_TOKEN = os.getenv('API_TOKEN', 'default-token-change-me')

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize processors
doc_processor = DocumentProcessor()
text_processor = create_text_processor()

# Initialize LLM processor
MODEL_NAME = os.getenv('MODEL_NAME', get_recommended_model())
logger.info(f"Initializing LLM processor with model: {MODEL_NAME}")
llm_processor = create_llm_processor(model_name=MODEL_NAME)

def allowed_file(filename):
    """Check if uploaded file has allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def authenticate_request():
    """Validate Bearer token authentication."""
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith("Bearer "):
        return False
    
    token = auth.split()[1]
    return token == API_TOKEN

def analyze_insurance_query(query: str, context: str, sources: list) -> tuple:
    """
    Simple rule-based analysis for insurance queries.
    This will be replaced with LLM-based analysis in the next step.
    """
    query_lower = query.lower()
    context_lower = context.lower()
    
    # Extract key information from query
    age_keywords = ["year", "old", "age"]
    surgery_keywords = ["surgery", "operation", "procedure"]
    location_keywords = ["pune", "mumbai", "delhi", "bangalore"]
    
    # Simple pattern matching
    decision = "Under Review"
    amount = "To be determined"
    justification = f"Found {len(sources)} relevant document sections. "
    
    # Check for coverage indicators
    if any(word in context_lower for word in ["covered", "eligible", "approved"]):
        decision = "Likely Approved"
        justification += "Context indicates coverage eligibility. "
        
        # Look for amount patterns
        import re
        amount_patterns = re.findall(r'₹[\d,]+|rs\.?\s*[\d,]+', context_lower)
        if amount_patterns:
            amount = amount_patterns[0]
            justification += f"Amount reference found: {amount}. "
    
    elif any(word in context_lower for word in ["not covered", "excluded", "rejected"]):
        decision = "Likely Rejected"
        justification += "Context indicates potential exclusion. "
    
    # Add source information
    justification += f"Based on analysis of documents: {', '.join(set(s['source'] for s in sources))}"
    
    return decision, amount, justification

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API information."""
    return jsonify({
        "service": "LLM Document Processing System",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "upload": "/upload (POST with Bearer token)",
            "query": "/query (POST with Bearer token)",
            "stats": "/stats (GET with Bearer token)"
        },
        "documentation": "See README.md for usage instructions",
        "web_interface": "Open simple_web_interface.html in your browser"
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "LLM Document Processing System",
        "version": "1.0.0"
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get vector store statistics."""
    if not authenticate_request():
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        vector_stats = text_processor.get_stats()
        llm_info = llm_processor.get_model_info()
        
        combined_stats = {
            "vector_store": vector_stats,
            "llm_model": llm_info,
            "system_status": {
                "document_processor": "available",
                "text_processor": "available", 
                "llm_processor": "available" if llm_processor.is_available() else "fallback mode"
            }
        }
        
        return jsonify(combined_stats)
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({"error": "Failed to get statistics"}), 500

@app.route('/upload', methods=['POST'])
def upload_document():
    """Upload and process a document for indexing."""
    if not authenticate_request():
        return jsonify({"error": "Unauthorized"}), 401
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        logger.info(f"File uploaded successfully: {filename}")
        
        # Extract text from document
        try:
            extracted_text, metadata = extract_text_from_document(filepath)
            
            # Validate extracted text
            if not doc_processor.validate_extracted_text(extracted_text):
                return jsonify({
                    "error": "Failed to extract meaningful text from document"
                }), 400
            
            # Get document statistics
            stats = doc_processor.get_document_stats(extracted_text)
            
            logger.info(f"Successfully processed document: {stats['words']} words, {stats['characters']} characters")
            
            # Chunk text and store in vector database
            try:
                chunks_added = text_processor.add_documents(
                    text=extracted_text,
                    source=filename,
                    metadata={
                        "filename": filename,
                        "original_metadata": metadata,
                        "extraction_stats": stats
                    }
                )
                
                # Get vector store statistics
                vector_stats = text_processor.get_stats()
                
                logger.info(f"Added {chunks_added} chunks to vector store")
                
                return jsonify({
                    "message": "Document processed and indexed successfully",
                    "filename": filename,
                    "status": "indexed",
                    "metadata": metadata,
                    "stats": stats,
                    "vector_store": {
                        "chunks_added": chunks_added,
                        "total_chunks": vector_stats["total_chunks"],
                        "embedding_model": vector_stats["embedding_model"]
                    },
                    "preview": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
                })
                
            except Exception as e:
                logger.error(f"Error adding to vector store: {str(e)}")
                return jsonify({
                    "error": f"Document processed but failed to index: {str(e)}"
                }), 500
            
        except Exception as e:
            logger.error(f"Error processing document {filename}: {str(e)}")
            return jsonify({
                "error": f"Failed to process document: {str(e)}"
            }), 500
    
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return jsonify({"error": "Failed to upload file"}), 500

@app.route('/query', methods=['POST'])
def process_query():
    """Process a natural language query against indexed documents."""
    if not authenticate_request():
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Query parameter required"}), 400
    
    query = data['query'].strip()
    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400
    
    try:
        logger.info(f"Processing query: {query}")
        
        # Search for relevant documents using semantic similarity
        try:
            relevant_docs = text_processor.search_similar(
                query=query,
                k=5,  # Get top 5 most relevant chunks
                score_threshold=0.3  # Minimum similarity threshold
            )
            
            if not relevant_docs:
                return jsonify({
                    "decision": "No relevant information found",
                    "amount": "N/A",
                    "justification": "No documents matched the query criteria. Please upload relevant documents first.",
                    "query": query,
                    "relevant_chunks": 0
                })
            
            # Extract relevant text for context
            context_texts = []
            source_info = []
            
            for doc in relevant_docs:
                context_texts.append(doc["text"])
                source_info.append({
                    "source": doc.get("source", "unknown"),
                    "chunk_id": doc.get("chunk_id", 0),
                    "similarity_score": doc.get("similarity_score", 0)
                })
            
            # For now, return structured information (LLM integration in next step)
            # This is a rule-based analysis for demonstration
            combined_context = "\n\n".join(context_texts[:3])  # Use top 3 chunks
            
            # Use LLM for intelligent analysis
            analysis_result = llm_processor.analyze_insurance_query(query, combined_context, source_info)
            
            decision = analysis_result.get("decision", "Under Review")
            amount = analysis_result.get("amount", "TBD")
            justification = analysis_result.get("justification", "Analysis in progress")
            analysis_method = analysis_result.get("analysis_method", "Unknown")
            
            response = {
                "decision": decision,
                "amount": amount,
                "justification": justification,
                "query": query,
                "relevant_chunks": len(relevant_docs),
                "sources": source_info[:3],  # Show top 3 sources
                "context_preview": combined_context[:500] + "..." if len(combined_context) > 500 else combined_context,
                "analysis_method": analysis_method,
                "llm_model": llm_processor.model_name if llm_processor.is_available() else "N/A"
            }
            
            return jsonify(response)
            
        except Exception as e:
            logger.error(f"Error during semantic search: {str(e)}")
            return jsonify({
                "error": f"Failed to search documents: {str(e)}"
            }), 500
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return jsonify({"error": "Failed to process query"}), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file size limit exceeded."""
    return jsonify({"error": "File too large"}), 413

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)