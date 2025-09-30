from datetime import datetime
from src.extensions import db
import json

class Analysis(db.Model):
    __tablename__ = 'analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # For easier querying
    summary = db.Column(db.Text)
    plagiarism_score = db.Column(db.Float, default=0.0)
    citation_count = db.Column(db.Integer, default=0)
    word_count = db.Column(db.Integer, default=0)
    quality_score = db.Column(db.Float, default=0.0)  # Overall quality score
    analysis_data_json = db.Column(db.Text)  # JSON string for all analysis results
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    citations = db.relationship('Citation', backref='analysis', lazy=True, cascade='all, delete-orphan')
    
    @property
    def analysis_data(self):
        """Get analysis data as Python dict."""
        if self.analysis_data_json:
            try:
                return json.loads(self.analysis_data_json)
            except json.JSONDecodeError:
                return {}
        return {}
    
    @analysis_data.setter
    def analysis_data(self, value):
        """Set analysis data from Python dict."""
        if value:
            self.analysis_data_json = json.dumps(value)
        else:
            self.analysis_data_json = None
    
    # Legacy properties for backward compatibility
    @property
    def critique(self):
        """Get critique from analysis data."""
        return self.analysis_data.get('critique_result', {})
    
    @property
    def plagiarism_details(self):
        """Get plagiarism details from analysis data."""
        return self.analysis_data.get('plagiarism_report', {})
    
    @property
    def fact_check_results(self):
        """Get fact check results from analysis data."""
        return self.analysis_data.get('fact_check_results', [])
    
    def to_dict(self, include_detailed=False):
        """Convert analysis to dictionary."""
        data = {
            'id': self.id,
            'document_id': self.document_id,
            'user_id': self.user_id,
            'summary': self.summary,
            'plagiarism_score': self.plagiarism_score,
            'citation_count': self.citation_count,
            'word_count': self.word_count,
            'quality_score': self.quality_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        # Include detailed analysis data if requested
        if include_detailed:
            data['analysis_data'] = self.analysis_data
            data['citations'] = [citation.to_dict() for citation in self.citations]
        
        return data
    
    def get_summary_stats(self):
        """Get summary statistics for the analysis."""
        return {
            'plagiarism_score': self.plagiarism_score,
            'citation_count': self.citation_count,
            'word_count': self.word_count,
            'quality_score': self.quality_score,
            'analysis_date': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Analysis {self.id} for Document {self.document_id}>'