# Research Paper Analysis API
# Research Paper Analysis Backend API

A comprehensive backend API for analyzing research papers using advanced academic analysis techniques including plagiarism detection, citation validation, summarization, and comprehensive academic critique.

## 🚀 Features

### Core Analysis Features
- **PDF Text Extraction**: Extract and process text content from PDF research papers
- **Plagiarism Detection**: AI-powered plagiarism checking using TF-IDF and cosine similarity
- **Citation Validation**: Verify citations against academic databases (Semantic Scholar, CrossRef) 
- **Text Summarization**: Generate summaries using transformer models (BART/T5)
- **Real Semantic Scholar Integration**: Direct API integration for citation validation (no API key required)

### Comprehensive Academic Analysis (NEW)
- **Academic Writing Quality Analysis**:
  - Structure and coherence evaluation
  - Argument flow assessment
  - Abstract quality analysis with component checking
- **Statistical Analysis Evaluation**:
  - Significance testing validation
  - Sample size adequacy assessment
  - Statistical assumptions checking
- **Citation Network Analysis**:
  - Citation pattern analysis and density
  - Impact factor assessment
  - Cross-reference validation
- **Literature Analysis**:
  - Research gap detection
  - Novelty and contribution assessment
  - Research positioning evaluation
- **Advanced Critique Features**:
  - Reproducibility assessment
  - Peer review quality metrics
  - Reference format validation

### Methodology & Argument Analysis (Priority 1 & 2)
- **Advanced Methodology Assessment**: Detection of research frameworks (experimental, survey, qualitative, quantitative, mixed-methods, systematic review)
- **Comprehensive Argument Evaluation**: Evidence-to-claim ratio analysis, logical flow assessment
- **Multi-dimensional Bias Detection**: Selection bias, confirmation bias, publication bias, reporting bias
- **Validity Assessment**: Internal, external, construct, and statistical validity evaluation

### System Features
- **User Authentication**: JWT-based authentication with role-based access control
- **Database Integration**: SQLite database for storing users, documents, and analysis results
- **RESTful API**: Clean REST endpoints for all functionality
- **Academic Grading System**: A-F grading with detailed scoring (0-100) for all analysis categories
- **Academic Recommendations**: AI-generated improvement suggestions for research papers

## 🏗️ Architecture

The backend follows a modular architecture with clear separation of concerns:

```
backend/
├── src/
│   ├── __init__.py              # Flask application factory
│   ├── models/                  # Database models
│   │   ├── user.py             # User model
│   │   ├── document.py         # Document model
│   │   ├── analysis.py         # Analysis results model
│   │   └── citation.py         # Citation model
│   ├── routes/                 # API endpoints
│   │   ├── auth.py            # Authentication routes
│   │   ├── simple_analyze.py  # Non-auth analysis endpoint
│   │   └── protected_analyze.py # Protected analysis endpoint
│   ├── services/              # Business logic
│   │   ├── pdf_service.py     # PDF processing
│   │   ├── plagiarism_service.py # Plagiarism detection
│   │   ├── citations_service.py  # Citation validation
│   │   ├── summarizer_service.py # Text summarization
│   │   └── critique_service.py   # Content critique
│   ├── utils/                 # Utilities
│   │   ├── auth_decorators.py # Authentication middleware
│   │   └── validators.py      # Input validation
│   └── extensions.py          # Flask extensions setup
├── config.py                  # Configuration settings
├── app.py                    # Application entry point
├── init_db.py               # Database initialization script
└── requirements.txt         # Python dependencies
```

## 🛠️ Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)
- SQLite (included with Python)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd research_critic-main/backend
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Setup

Create a `.env` file in the backend directory:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Database Configuration
SQLALCHEMY_DATABASE_URI=sqlite:///C:/full/path/to/backend/instance/app.db

# Security Keys
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# API Keys (Optional - will use real Semantic Scholar API without keys)
SEMANTIC_SCHOLAR_API_KEY=not-required-api-is-free
GOOGLE_FACT_CHECK_API_KEY=your-google-fact-check-key

# Upload Settings
UPLOAD_DIR=uploads
MAX_UPLOAD_MB=25
ALLOWED_EXT=.pdf

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Feature Flags
USE_HF_SUMMARIZER=true
ALLOW_GUEST_UPLOADS=false
```

### 5. Database Initialization

```bash
# Initialize database with tables
python init_db.py

# Follow prompts to create an admin user (optional)
```

## 🚀 Running the Application

### Start the Server

```bash
# Set environment variable for database (Windows)
$env:SQLALCHEMY_DATABASE_URI="sqlite:///C:/full/path/to/backend/instance/app.db"

# Run the application
python app.py
```

The server will start on `http://0.0.0.0:5000`

### Verify Installation

Test the health endpoint:

```bash
curl http://127.0.0.1:5000/health
```

Expected response:
```json
{
  "status": "success",
  "message": "Research Paper Analysis API is running"
}
```

## 🔐 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | User login | No |
| POST | `/api/auth/refresh` | Refresh access token | Yes (refresh token) |
| POST | `/api/auth/logout` | User logout | Yes |
| GET | `/api/auth/profile` | Get user profile | Yes |
| PUT | `/api/auth/profile` | Update user profile | Yes |

### Analysis Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/analyze` | Simple analysis (no auth) | No |
| POST | `/api/protected/analyze` | Full analysis with storage | Yes |
| GET | `/api/health` | Health check | No |

### Authentication Examples

#### Register a User

```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

#### Login

```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

#### Access Protected Endpoint

```bash
curl -X POST http://127.0.0.1:5000/api/protected/analyze \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@path/to/your/paper.pdf"
```

## 📊 Comprehensive Analysis Response Format

The API provides comprehensive academic analysis with the following structure:

### Response Overview

```json
{
  "document_id": 1,
  "analysis_id": 1,
  "summary": "AI-generated summary of the paper...",
  "plagiarism": {
    "plagiarism_score": 15.2,
    "risk_level": "Low"
  },
  "citations": {
    "total_citations": 25,
    "quality_score": 85.0,
    "validated_citations": 22
  },
  "critique": {
    // Comprehensive academic analysis
  },
  "overall_quality_score": 78.5,
  "stats": {
    "word_count": 5420,
    "analysis_date": "2024-01-15T10:30:00Z"
  }
}
```

### Comprehensive Critique Structure

The `critique` object contains detailed academic analysis across 5 major categories:

#### 1. Academic Writing Quality Analysis

```json
"writing_quality_analysis": {
  "structure_coherence": {
    "sections_found": ["introduction", "methods", "results", "discussion"],
    "coherence_indicators": 15,
    "score": 82,
    "assessment": "Good"
  },
  "argument_flow": {
    "logical_connectors": {
      "causal": 8,
      "contrast": 5,
      "addition": 12
    },
    "total_flow_indicators": 25,
    "evidence_density": 0.0045,
    "score": 75.0,
    "assessment": "Strong"
  },
  "abstract_quality": {
    "components": {
      "background": true,
      "objective": true,
      "methods": true,
      "results": true,
      "conclusion": true
    },
    "word_count": 250,
    "score": 90.0,
    "assessment": "Excellent"
  },
  "overall_writing_score": 82.3
}
```

#### 2. Statistical Analysis Evaluation

```json
"statistical_analysis": {
  "significance_testing": {
    "statistical_tests_found": ["t_test", "anova"],
    "p_values_reported": 5,
    "effect_sizes_reported": ["cohen's d"],
    "confidence_intervals": true,
    "score": 85,
    "assessment": "Comprehensive"
  },
  "sample_size_adequacy": {
    "sample_sizes_found": [120, 95],
    "largest_sample": 120,
    "sample_adequacy": "Large",
    "power_analysis_mentioned": true,
    "score": 90.0,
    "assessment": "Strong"
  },
  "statistical_assumptions": {
    "assumptions_checked": {
      "normality": true,
      "homogeneity": true,
      "independence": false
    },
    "assumptions_count": 2,
    "score": 60,
    "assessment": "Partial"
  },
  "overall_statistical_score": 78.3
}
```

#### 3. Citation Network Analysis

```json
"citation_network_analysis": {
  "citation_patterns": {
    "citation_density": 4.6,
    "total_citations": 25,
    "recent_citations_ratio": 0.68,
    "average_citation_age": 3.2,
    "score": 85.0,
    "assessment": "Excellent"
  },
  "impact_assessment": {
    "high_impact_citations": 8,
    "citation_diversity": 24,
    "impact_ratio": 0.32,
    "score": 75.0,
    "assessment": "High"
  },
  "cross_reference_validation": {
    "table_references": 3,
    "figure_references": 5,
    "total_internal_references": 12,
    "score": 70,
    "assessment": "Adequate"
  },
  "overall_citation_score": 76.7
}
```

#### 4. Literature Analysis

```json
"literature_analysis": {
  "research_gaps": {
    "gap_indicators_found": 8,
    "specific_gaps_mentioned": 3,
    "score": 75,
    "assessment": "Well-identified"
  },
  "novelty_assessment": {
    "novelty_claims": 5,
    "contribution_mentions": 8,
    "innovation_indicators": 12,
    "score": 80,
    "assessment": "Strong novelty"
  },
  "research_positioning": {
    "field_positioning": 15,
    "comparison_with_existing": 6,
    "future_directions": 4,
    "score": 85,
    "assessment": "Well-positioned"
  },
  "overall_literature_score": 80.0
}
```

#### 5. Advanced Critique Features

```json
"advanced_critique_features": {
  "reproducibility_assessment": {
    "reproducibility_indicators": 4,
    "data_sharing_mentions": 2,
    "method_detail_level": 25,
    "score": 70,
    "assessment": "Moderately reproducible"
  },
  "peer_review_metrics": {
    "peer_review_mentions": 1,
    "quality_indicators": 2,
    "journal_quality_hints": 1,
    "score": 45,
    "assessment": "Standard review"
  },
  "reference_format_validation": {
    "total_references": 25,
    "format_consistency_ratio": 0.92,
    "doi_presence_ratio": 0.80,
    "score": 88.0,
    "assessment": "Excellent formatting"
  },
  "overall_advanced_score": 67.7
}
```

#### Overall Assessment & Recommendations

```json
"overall_assessment": {
  "overall_score": 78.5,
  "grade": "B+",
  "category": "Good academic work"
},
"academic_recommendations": [
  "Enhance methodology section with detailed procedures and statistical approach",
  "Address validity concerns by discussing internal/external validity",
  "Provide more empirical evidence to support claims and conclusions"
],
"quality_grade": {
  "grade": "B+",
  "description": "Good academic work"
}
```

### Scoring System

- **Overall Score**: Weighted average (0-100) across all analysis categories
- **Grade Assignment**: 
  - A+ (90-100): Outstanding academic quality
  - A (85-89): Excellent academic standards  
  - B+ (80-84): Very good quality
  - B (70-79): Good academic work
  - C+ (60-69): Satisfactory quality
  - C (55-59): Marginal quality
  - F (0-54): Fails academic standards

### Methodology Frameworks Detected

The system automatically detects research methodologies:
- **Experimental**: randomized, control group, treatment
- **Survey**: questionnaire, cross-sectional, longitudinal 
- **Qualitative**: interview, focus group, case study
- **Quantitative**: statistical, regression, correlation
- **Mixed Methods**: triangulation, concurrent, sequential
- **Systematic Review**: meta-analysis, literature review

## 🧪 Testing

### Run Health Check

```bash
python -c "
import requests
response = requests.get('http://127.0.0.1:5000/health')
print(response.json())
"
```

### Test Authentication

```bash
python -c "
import requests
import json

# Register
register_data = {
    'name': 'Test User',
    'email': 'test@example.com',
    'password': 'test123'
}
response = requests.post('http://127.0.0.1:5000/api/auth/register', json=register_data)
print('Register:', response.status_code)

# Login
login_data = {
    'email': 'test@example.com',
    'password': 'test123'
}
response = requests.post('http://127.0.0.1:5000/api/auth/login', json=login_data)
print('Login:', response.status_code)
print('Token:', response.json().get('access_token', 'Failed')[:50] + '...')
"
```

## 🔧 Configuration

### Database Configuration

The application uses SQLite by default. To use a different database, update the `SQLALCHEMY_DATABASE_URI` in your `.env` file:

```env
# PostgreSQL
SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost/dbname

# MySQL
SQLALCHEMY_DATABASE_URI=mysql://user:password@localhost/dbname
```

### API Keys Configuration

The application can work with real academic APIs:

- **Semantic Scholar API**: **FREE and no API key required!** The app uses the real Semantic Scholar API for citation validation
- **Google Fact Check API**: Optional, for fact-checking claims (uses mock data if not provided)
- **HuggingFace Models**: Downloaded automatically for summarization

### Upload Configuration

Configure file upload settings in `.env`:

```env
UPLOAD_DIR=uploads
MAX_UPLOAD_MB=25
ALLOWED_EXT=.pdf
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```
   sqlite3.OperationalError: unable to open database file
   ```
   **Solution**: Ensure the database path is absolute and the directory exists:
   ```bash
   mkdir -p instance
   export SQLALCHEMY_DATABASE_URI="sqlite:///$(pwd)/instance/app.db"
   ```

2. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'flask'
   ```
   **Solution**: Activate virtual environment and install dependencies:
   ```bash
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **JWT Token Errors**
   ```
   jwt.exceptions.DecodeError: Not enough segments
   ```
   **Solution**: Ensure you're passing the Authorization header correctly:
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN_HERE" ...
   ```

4. **File Upload Errors**
   ```
   413 Request Entity Too Large
   ```
   **Solution**: Check file size and `MAX_UPLOAD_MB` setting in configuration.

### Debug Mode

Enable debug mode for development:

```bash
export DEBUG=True
python app.py
```

### Logs

Check application logs for detailed error information:

```bash
tail -f logs/app.log        # Application logs
tail -f logs/error.log      # Error logs only
```

## 🔒 Security Considerations

- JWT tokens expire after 1 hour (configurable)
- Passwords are hashed using Werkzeug's security functions
- File uploads are validated for type and size
- CORS is configured for frontend integration
- SQL injection protection via SQLAlchemy ORM

## 📚 Dependencies

### Core Dependencies

- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM
- **Flask-JWT-Extended**: JWT authentication
- **Flask-CORS**: Cross-origin resource sharing
- **PyPDF2**: PDF text extraction
- **scikit-learn**: Machine learning for plagiarism detection
- **transformers**: Hugging Face models for summarization
- **requests**: HTTP client for API calls

### Development Dependencies

- **python-dotenv**: Environment variable management
- **reportlab**: PDF generation for reports

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

1. Check the troubleshooting section above
2. Review the API documentation
3. Check the logs for error details
4. Create an issue in the repository

## 🔄 API Response Formats

### Success Response

```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "data": { ... }
}
```

### Error Response

```json
{
  "error": "Description of the error",
  "code": 400
}
```

### Analysis Response

```json
{
  "summary": "Generated summary text...",
  "plagiarism": 15,
  "citations": [
    {
      "raw": "Smith et al. (2023)",
      "status": "verified",
      "title": "Paper Title"
    }
  ],
  "stats": {
    "word_count": 1500,
    "plagiarism_percent": 15,
    "citations_count": 8
  }
}
```