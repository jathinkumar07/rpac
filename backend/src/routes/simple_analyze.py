from flask import Blueprint, request, jsonify, current_app
import logging
from src.services.pdf_service import PDFService
from src.services.plagiarism_service import PlagiarismService
from src.services.citations_service import CitationsService
from src.services.summarizer_service import SummarizerService
from src.services.critique_service import CritiqueService
from src.utils.auth_decorators import validate_file_upload

logger = logging.getLogger(__name__)
simple_analyze_bp = Blueprint("simple_analyze", __name__)

@simple_analyze_bp.route("/analyze", methods=["POST"])
@validate_file_upload
def analyze_paper():
    """Simple analysis endpoint (no authentication required - compatible with original app_working.py)"""
    try:
        logger.info("Starting simple paper analysis request")
        
        file = request.files["file"]
        
        # Initialize services
        pdf_service = PDFService(current_app.config.get('UPLOAD_DIR', './uploads'))
        plagiarism_service = PlagiarismService()
        citations_service = CitationsService()
        summarizer_service = SummarizerService()
        critique_service = CritiqueService()
        
        try:
            # Process PDF
            text = pdf_service.process_uploaded_pdf(file)
            logger.info(f"Extracted {len(text)} characters from PDF")
            
            # Perform analysis
            logger.info("Generating summary")
            summary = summarizer_service.summarize_text(text)
            
            logger.info("Detecting plagiarism")
            plagiarism_score = plagiarism_service.detect_plagiarism(text)
            
            logger.info("Extracting and validating citations")
            citations = citations_service.extract_citations(text)
            citation_results = citations_service.validate_citations(citations)
            
            logger.info("Generating critique")
            critique_result = critique_service.critique_paper(text)
            
            # Prepare response (compatible with original app_working.py format)
            response = {
                "summary": summary,
                "plagiarism": plagiarism_score,
                "citations": citation_results,
                "fact_check": {
                    "facts": []  # Placeholder for fact check results
                },
                "stats": {
                    "word_count": critique_service.count_words(text),
                    "plagiarism_percent": plagiarism_score,
                    "citations_count": len(citation_results)
                }
            }
            
            logger.info("Simple analysis completed successfully")
            return jsonify(response), 200
            
        except Exception as e:
            logger.error(f"Analysis processing error: {e}")
            return jsonify({"error": f"Analysis failed: {str(e)}"}), 500
    
    except Exception as e:
        logger.error(f"Error in simple analyze_paper: {e}")
        return jsonify({"error": "Internal server error"}), 500

@simple_analyze_bp.route("/health", methods=["GET"])
def health_check():
    """Health check for simple analyze service"""
    return jsonify({
        "status": "healthy",
        "service": "simple_analyze",
        "message": "Simple analyze service is running"
    }), 200
