from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
import os
from datetime import datetime

from src.extensions import db
from src.models.user import User
from src.models.document import Document
from src.models.analysis import Analysis
from src.services.pdf_service import PDFService
from src.services.plagiarism_service import PlagiarismService
from src.services.citations_service import CitationsService
from src.services.summarizer_service import SummarizerService
from src.services.critique_service import CritiqueService

logger = logging.getLogger(__name__)

protected_analyze_bp = Blueprint('protected_analyze', __name__)

@protected_analyze_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze_paper():
    """Protected analysis endpoint for authenticated users"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        logger.info(f"Starting paper analysis request for user: {user.email}")
        
        # Check if file is present
        if "file" not in request.files:
            logger.error("No file uploaded")
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files["file"]
        if file.filename == '':
            logger.error("No file selected")
            return jsonify({"error": "No file selected"}), 400
        
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
            
            # Create document record
            document = Document(
                user_id=current_user_id,
                filename=file.filename,
                file_size=len(text),
                content_preview=text[:500]  # Store first 500 chars as preview
            )
            db.session.add(document)
            db.session.flush()  # Get document ID
            
            # Perform analysis
            logger.info("Generating summary")
            summary = summarizer_service.summarize_text(text)
            
            logger.info("Detecting plagiarism")
            plagiarism_report = plagiarism_service.get_plagiarism_report(text)
            
            logger.info("Analyzing citations")
            citations_report = citations_service.get_citations_report(text)
            
            logger.info("Generating critique")
            critique_result = critique_service.critique_paper(text)
            
            # Calculate overall quality score
            quality_metrics = {
                "plagiarism_score": plagiarism_report.get("plagiarism_score", 0),
                "citation_quality": citations_report.get("quality_score", 0),
                "methodology_score": critique_result.get("methodology_score", 0),
                "structure_score": critique_result.get("structure_score", 0)
            }
            
            overall_quality = (
                (100 - quality_metrics["plagiarism_score"]) * 0.3 +
                quality_metrics["citation_quality"] * 0.3 +
                quality_metrics["methodology_score"] * 0.2 +
                quality_metrics["structure_score"] * 0.2
            )
            
            # Save analysis results
            analysis = Analysis(
                document_id=document.id,
                user_id=current_user_id,
                summary=summary,
                plagiarism_score=plagiarism_report.get("plagiarism_score", 0),
                citation_count=citations_report.get("total_citations", 0),
                word_count=critique_service.count_words(text),
                quality_score=round(overall_quality, 1),
                analysis_data={
                    "plagiarism_report": plagiarism_report,
                    "citations_report": citations_report,
                    "critique_result": critique_result,
                    "quality_metrics": quality_metrics
                }
            )
            db.session.add(analysis)
            
            # Update document with analysis reference
            document.latest_analysis_id = analysis.id
            
            db.session.commit()
            
            # Prepare response
            response = {
                "document_id": document.id,
                "analysis_id": analysis.id,
                "summary": summary,
                "plagiarism": plagiarism_report,
                "citations": citations_report,
                "critique": critique_result,
                "quality_metrics": quality_metrics,
                "overall_quality_score": round(overall_quality, 1),
                "stats": {
                    "word_count": critique_service.count_words(text),
                    "analysis_date": analysis.created_at.isoformat()
                }
            }
            
            logger.info(f"Analysis completed successfully for user: {user.email}")
            return jsonify(response), 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Analysis processing error: {e}")
            return jsonify({"error": f"Analysis failed: {str(e)}"}), 500
    
    except Exception as e:
        logger.error(f"Error in analyze_paper: {e}")
        return jsonify({"error": "Internal server error"}), 500

@protected_analyze_bp.route('/history', methods=['GET'])
@jwt_required()
def get_analysis_history():
    """Get user's analysis history"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)  # Max 50 per page
        
        # Query user's documents with analyses
        documents_query = Document.query.filter_by(user_id=current_user_id).order_by(
            Document.created_at.desc()
        )
        
        documents_pagination = documents_query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        documents_data = []
        for doc in documents_pagination.items:
            doc_data = {
                "id": doc.id,
                "filename": doc.filename,
                "created_at": doc.created_at.isoformat(),
                "file_size": doc.file_size,
                "content_preview": doc.content_preview
            }
            
            # Get latest analysis if exists
            if doc.latest_analysis_id:
                analysis = Analysis.query.get(doc.latest_analysis_id)
                if analysis:
                    doc_data["latest_analysis"] = {
                        "id": analysis.id,
                        "quality_score": analysis.quality_score,
                        "plagiarism_score": analysis.plagiarism_score,
                        "word_count": analysis.word_count,
                        "created_at": analysis.created_at.isoformat()
                    }
            
            documents_data.append(doc_data)
        
        return jsonify({
            "documents": documents_data,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": documents_pagination.total,
                "pages": documents_pagination.pages,
                "has_next": documents_pagination.has_next,
                "has_prev": documents_pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching analysis history: {e}")
        return jsonify({"error": "Failed to fetch analysis history"}), 500

@protected_analyze_bp.route('/analysis/<int:analysis_id>', methods=['GET'])
@jwt_required()
def get_analysis_details(analysis_id):
    """Get detailed analysis results"""
    try:
        current_user_id = get_jwt_identity()
        
        # Find analysis and verify ownership
        analysis = Analysis.query.filter_by(
            id=analysis_id,
            user_id=current_user_id
        ).first()
        
        if not analysis:
            return jsonify({"error": "Analysis not found"}), 404
        
        # Get associated document
        document = Document.query.get(analysis.document_id)
        
        response = {
            "analysis": {
                "id": analysis.id,
                "created_at": analysis.created_at.isoformat(),
                "summary": analysis.summary,
                "plagiarism_score": analysis.plagiarism_score,
                "citation_count": analysis.citation_count,
                "word_count": analysis.word_count,
                "quality_score": analysis.quality_score,
                "detailed_results": analysis.analysis_data
            },
            "document": {
                "id": document.id,
                "filename": document.filename,
                "file_size": document.file_size,
                "created_at": document.created_at.isoformat()
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error fetching analysis details: {e}")
        return jsonify({"error": "Failed to fetch analysis details"}), 500

@protected_analyze_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """Get user's analysis statistics"""
    try:
        current_user_id = get_jwt_identity()
        
        # Count documents and analyses
        total_documents = Document.query.filter_by(user_id=current_user_id).count()
        total_analyses = Analysis.query.filter_by(user_id=current_user_id).count()
        
        # Get average quality score
        from sqlalchemy import func
        avg_quality = db.session.query(func.avg(Analysis.quality_score)).filter_by(
            user_id=current_user_id
        ).scalar() or 0
        
        # Get recent activity (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_analyses = Analysis.query.filter(
            Analysis.user_id == current_user_id,
            Analysis.created_at >= thirty_days_ago
        ).count()
        
        return jsonify({
            "total_documents": total_documents,
            "total_analyses": total_analyses,
            "average_quality_score": round(avg_quality, 1),
            "recent_analyses_30d": recent_analyses
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching user stats: {e}")
        return jsonify({"error": "Failed to fetch statistics"}), 500
