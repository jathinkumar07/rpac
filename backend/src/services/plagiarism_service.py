import re
import requests
import json
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List
from collections import Counter

logger = logging.getLogger(__name__)

class PlagiarismService:
    """Service for detecting plagiarism using Semantic Scholar API"""
    
    def __init__(self, semantic_scholar_base="https://api.semanticscholar.org/graph/v1/paper/search"):
        self.semantic_scholar_base = semantic_scholar_base
    
    def safe_api_request(self, url, timeout=10):
        """Make API request with proper error handling"""
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logger.warning(f"API request timeout for URL: {url}")
            return None
        except requests.exceptions.RequestException as e:
            logger.warning(f"API request failed for URL: {url}, Error: {e}")
            return None
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON response from URL: {url}")
            return None
    
    def detect_plagiarism(self, text):
        """Detect plagiarism using Semantic Scholar API with fallback"""
        try:
            # Clean and prepare text
            words = re.findall(r'\b\w+\b', text.lower())
            common_words = [w for w in words if len(w) > 4]
            
            if len(common_words) < 3:
                return 0
            
            # Use first 6 meaningful words as keywords
            keywords = " ".join(common_words[:6])
            
            # Search for similar papers
            params = {
                "query": keywords,
                "fields": "title,abstract",
                "limit": 5
            }
            
            response = requests.get(self.semantic_scholar_base, params=params, timeout=10)
            
            abstracts = []
            if response.status_code == 200:
                data = response.json()
                if "data" in data:
                    for paper in data["data"]:
                        abstract = paper.get("abstract", "")
                        if abstract and len(abstract) > 50:
                            abstracts.append(abstract)
            
            if not abstracts:
                logger.info("No abstracts found for comparison")
                return 0
            
            # Calculate similarity
            documents = [text] + abstracts
            
            try:
                vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
                tfidf_matrix = vectorizer.fit_transform(documents)
                similarity_scores = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])[0]
                max_score = max(similarity_scores) * 100
                return round(max_score, 2) if max_score > 10 else 0
            except Exception as e:
                logger.warning(f"Error calculating similarity: {e}")
                return 0
                
        except Exception as e:
            logger.error(f"Error in plagiarism detection: {e}")
            return 0
    
    def get_plagiarism_report(self, text):
        """Get detailed plagiarism report"""
        plagiarism_score = self.detect_plagiarism(text)
        
        # Determine severity
        if plagiarism_score < 15:
            severity = "Low"
            message = "Minimal similarity detected with existing academic works."
        elif plagiarism_score < 40:
            severity = "Moderate"
            message = "Some similarity detected. Review citations and paraphrasing."
        else:
            severity = "High"
            message = "Significant similarity detected. Immediate review required."
        
        return {
            "plagiarism_score": plagiarism_score,
            "severity": severity,
            "message": message,
            "recommendation": self._get_recommendation(plagiarism_score)
        }
    
    def _get_recommendation(self, score):
        """Get recommendation based on plagiarism score"""
        if score < 15:
            return "Document appears to be original. Continue with submission."
        elif score < 40:
            return "Review citations and ensure proper attribution of sources."
        else:
            return "Significant revision required. Check for proper citations and paraphrasing."

# Legacy functions for backward compatibility
def _sentences(text: str) -> List[str]:
    # simple sentence split; avoids NLTK dependency here
    parts = re.split(r'(?<=[.!?])\s+', text)
    return [p.strip() for p in parts if len(p.strip()) > 0]

def _ngrams(tokens: List[str], n: int) -> List[str]:
    return [' '.join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

def _tokenize(s: str) -> List[str]:
    return re.findall(r"[A-Za-z0-9']+", s.lower())

def check_plagiarism(text: str) -> Dict:
    """
    Heuristic, offline plagiarism score:
      - measures internal repetition via 7-gram shingles
      - discounts very short/boilerplate lines
    Returns: {"plagiarism_score": float(0..1), "matching_sources": []}
    """
    if not text or len(text) < 200:
        return {"plagiarism_score": 0.0, "matching_sources": []}

    sents = [s for s in _sentences(text) if len(s) > 25]
    if len(sents) < 5:
        return {"plagiarism_score": 0.0, "matching_sources": []}

    all_shingles: Counter = Counter()
    for s in sents:
        toks = _tokenize(s)
        sh = _ngrams(toks, 7)
        all_shingles.update(sh)

    if not all_shingles:
        score = 0.0
    else:
        dup = sum(c for c in all_shingles.values() if c > 1)
        total = sum(all_shingles.values())
        score = min(1.0, dup / max(1, total))

    logger.info("Heuristic plagiarism score: %.3f", score)
    return {"plagiarism_score": float(score), "matching_sources": []}

# Backwards-compat function some routes call
def check(text: str) -> int:
    """Return percent [0..100] for legacy callers."""
    res = check_plagiarism(text)
    return int(round(100 * float(res.get("plagiarism_score", 0.0))))
