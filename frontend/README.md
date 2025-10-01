# AI Research Critic - Frontend

A modern React TypeScript frontend for the AI Research Critic application, providing comprehensive academic paper analysis with professional-grade critique, plagiarism detection, citation validation, and detailed academic recommendations.

## Features

### Core Features
- **Drag & Drop Upload**: Intuitive PDF file upload with validation
- **Real-time Analysis**: Connect to Flask backend for comprehensive document processing
- **Responsive Design**: Mobile-first design using TailwindCSS
- **Modern UI**: Clean, professional interface with loading states and progress indicators
- **Academic Dashboard**: Professional analysis visualization with scoring system
- **Download Results**: Export comprehensive analysis results as JSON

### Comprehensive Analysis Display (NEW)
- **Overall Academic Quality Score**: A-F grading system with detailed breakdown
- **5 Major Analysis Categories**:
  - ✍️ Academic Writing Quality (structure, argument flow, abstract quality)
  - 📊 Statistical Analysis (significance testing, sample size, assumptions)
  - 📚 Citation Network Analysis (patterns, impact factors, cross-references)
  - 📚 Literature Analysis (gap detection, novelty, positioning)
  - 🔬 Advanced Critique Features (reproducibility, peer review, reference format)
- **Academic Recommendations**: AI-generated improvement suggestions
- **Detailed Scoring**: Color-coded progress indicators for each analysis component
- **Professional Visualization**: Academic-grade results presentation

### Enhanced Results Display
- **Methodology Framework Detection**: Shows detected research methodologies
- **Bias Analysis**: Multi-dimensional bias detection with severity indicators
- **Validity Assessment**: Internal, external, construct, and statistical validity scores
- **Citation Network Metrics**: Impact assessment and cross-reference validation
- **Reproducibility Assessment**: Data sharing and method transparency evaluation

## Tech Stack

- **React 18** with TypeScript for type safety
- **TailwindCSS** for responsive styling
- **React Router** for client-side routing
- **Axios** for API communication
- **Modern ES6+** features and hooks

## Prerequisites

- Node.js 16+ and npm
- Backend Flask server running on port 5000

## Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
# Copy .env file is already created with:
# REACT_APP_API_URL=http://localhost:5000
```

## Development

Start the development server:
```bash
npm start
```

The app will be available at `http://localhost:3000`

## Production Build

Create production build:
```bash
npm run build
```

## Project Structure

```
src/
├── components/
│   └── Navbar.tsx          # Navigation component
├── pages/
│   ├── Home.tsx            # Upload and analysis page
│   ├── Results.tsx         # Analysis results display
│   └── About.tsx           # App information page
├── services/
│   └── api.ts              # API service layer
├── types/
│   └── index.ts            # TypeScript interfaces
├── App.tsx                 # Main app component
└── index.tsx               # App entry point
```

## API Integration

The frontend connects to the Flask backend via the `/analyze` endpoint:

- **Endpoint**: `POST /analyze`
- **Content-Type**: `multipart/form-data`
- **File**: PDF document (max 10MB)
- **Response**: Analysis results including summary, plagiarism score, citations, and fact-check results

## Features Overview

### Home Page
- Drag-and-drop PDF upload
- File validation (PDF only, ≤10MB)
- Loading spinner during analysis
- Error handling and user feedback

### Results Page
- **Academic Quality Dashboard**: Overall score, grade, and category assessment
- **Comprehensive Analysis Sections**: 5 major academic analysis categories
- **Statistics Overview**: Enhanced metrics with methodology and validity scores
- **AI-generated Summary**: Intelligent content summarization
- **Plagiarism Analysis**: Risk assessment with detailed scoring
- **Writing Quality Analysis**: Structure, coherence, and argument flow evaluation
- **Statistical Analysis**: Significance testing, sample size, and assumptions validation
- **Citation Network Analysis**: Pattern analysis, impact assessment, cross-reference validation
- **Literature Analysis**: Gap detection, novelty assessment, research positioning
- **Advanced Critique Features**: Reproducibility, peer review quality, reference formatting
- **Academic Recommendations**: Personalized improvement suggestions
- **Download Functionality**: Export comprehensive analysis results

### About Page
- Feature descriptions
- Technology stack information
- Usage instructions

## Environment Variables

- `REACT_APP_API_URL`: Backend API URL (default: http://localhost:5000)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
