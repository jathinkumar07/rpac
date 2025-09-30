from datetime import datetime
from src.extensions import db

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)  # File size in bytes
    content_preview = db.Column(db.Text)  # First 500 chars for preview
    stored_path = db.Column(db.String(500))  # Optional: if storing files
    title = db.Column(db.String(500))
    extracted_text = db.Column(db.Text)  # Store extracted PDF text
    word_count = db.Column(db.Integer)
    latest_analysis_id = db.Column(db.Integer, db.ForeignKey('analyses.id'))  # Reference to latest analysis
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    analyses = db.relationship('Analysis', backref='document', lazy=True, cascade='all, delete-orphan', foreign_keys='Analysis.document_id')
    latest_analysis = db.relationship('Analysis', foreign_keys=[latest_analysis_id], post_update=True)
    
    def to_dict(self, include_text=False):
        """Convert document to dictionary."""
        data = {
            'id': self.id,
            'filename': self.filename,
            'file_size': self.file_size,
            'content_preview': self.content_preview,
            'title': self.title,
            'word_count': self.word_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'latest_analysis_id': self.latest_analysis_id
        }
        
        # Only include extracted text if explicitly requested (for authorized users)
        if include_text and self.extracted_text:
            data['extracted_text'] = self.extracted_text
            
        return data
    
    def __repr__(self):
        return f'<Document {self.filename}>'