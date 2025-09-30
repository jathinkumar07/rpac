# Research Paper Analysis API

A comprehensive backend API for analyzing research papers using machine learning techniques including plagiarism detection, citation validation, summarization, and content critique.

## 🚀 Features

- **PDF Text Extraction**: Extract and process text content from PDF research papers
- **Plagiarism Detection**: AI-powered plagiarism checking using TF-IDF and cosine similarity
- **Citation Validation**: Verify citations against academic databases (Semantic Scholar, CrossRef)
- **Text Summarization**: Generate summaries using transformer models (BART/T5)
- **Content Critique**: AI-powered academic paper review and feedback
- **User Authentication**: JWT-based authentication with role-based access control
- **Database Integration**: SQLite database for storing users, documents, and analysis results
- **RESTful API**: Clean REST endpoints for all functionality

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

# API Keys (Optional - will use mock data if not provided)
SEMANTIC_SCHOLAR_API_KEY=your-semantic-scholar-key
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

The application can work without API keys by using mock data:

- **Semantic Scholar API**: For citation validation
- **Google Fact Check API**: For fact-checking claims
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