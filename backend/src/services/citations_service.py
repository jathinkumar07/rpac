import re
import requests
import json
import logging
from typing import List, Dict
import os

logger = logging.getLogger(__name__)

class CitationsService:
    """Service for extracting and validating citations"""
    
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
    
    def extract_citations(self, text):
        """Extract citations from text"""
        try:
            # Look for references section
            text_lower = text.lower()
            references_patterns = ["references", "bibliography", "works cited", "citations"]
            
            references_start = -1
            for pattern in references_patterns:
                pos = text_lower.find(pattern)
                if pos != -1:
                    references_start = pos
                    break
            
            if references_start == -1:
                # Try to find numbered references in text
                numbered_refs = re.findall(r'\[\d+\].*?(?=\[\d+\]|$)', text, re.DOTALL)
                return numbered_refs[:10] if numbered_refs else []
            
            # Extract references section
            references_text = text[references_start:]
            references = []
            
            # Split by common reference patterns
            ref_lines = references_text.split("\n")
            for line in ref_lines[:20]:  # Limit to first 20 lines
                line = line.strip()
                if len(line) > 20 and not line.lower().startswith(('references', 'bibliography')):
                    references.append(line)
                    if len(references) >= 10:
                        break
            
            return references
        except Exception as e:
            logger.error(f"Error extracting citations: {e}")
            return []
    
    def clean_citation(self, citation):
        """Clean and extract title from citation with better parsing"""
        try:
            citation = citation.replace("\n", " ").strip()
            
            # Remove leading numbers like "1. " or "[1] " 
            citation = re.sub(r'^\s*\d+\.\s*', '', citation)
            citation = re.sub(r'^\s*\[\d+\]\s*', '', citation)
            
            # Try to extract title from quotes first
            title_match = re.search(r'"([^"]+)"', citation)
            if title_match:
                return title_match.group(1)
            
            # Try to extract title from italic markers
            italic_match = re.search(r'\*([^*]+)\*', citation)
            if italic_match:
                return italic_match.group(1)
            
            # Try to find title after authors and year: "Author (2023). Title. Journal"
            # Look for pattern: ") or year. then title until next period
            title_after_year = re.search(r'\)\.[\s]*([^.]+)\.', citation)
            if title_after_year:
                title = title_after_year.group(1).strip()
                if len(title) > 10:
                    return title
            
            # Try to find title after year pattern: "Author et al. (2023) Title. Journal"
            title_after_paren = re.search(r'\(\d{4}[a-z]?\)[\s]*([^.]+)\.', citation)
            if title_after_paren:
                title = title_after_paren.group(1).strip()
                if len(title) > 10:
                    return title
            
            # Try to extract the longest reasonable segment as title
            parts = [p.strip() for p in citation.split('.') if len(p.strip()) > 10]
            if len(parts) >= 2:
                # Usually title is the second part after author info
                for part in parts[1:3]:  # Check 2nd and 3rd parts
                    # Skip parts that look like journal names or page numbers
                    if not re.search(r'\b(pp?\.|vol\.|\d+\(\d+\)|journal|proceedings)', part, re.IGNORECASE):
                        if len(part) > 10:
                            return part
            
            # Fallback: return first long part
            if parts and len(parts[0]) > 10:
                return parts[0]
            
            # Last resort: return original if reasonable length
            return citation if len(citation) > 5 else ""
            
        except Exception as e:
            logger.warning(f"Error cleaning citation: {e}")
            return citation
    
    def validate_citations(self, citations):
        """Validate citations using real Semantic Scholar API (no API key required)"""
        citation_results = []
        
        for i, citation in enumerate(citations[:10]):  # Limit to 10 citations
            try:
                cleaned_title = self.clean_citation(citation)
                if not cleaned_title or len(cleaned_title) < 5:
                    citation_results.append({
                        "reference": citation,
                        "valid": False,
                        "reason": "Could not extract title"
                    })
                    continue
                
                # Use real Semantic Scholar API (free, no key required)
                params = {
                    "query": cleaned_title,
                    "fields": "title,authors,year,venue",
                    "limit": 3
                }
                
                try:
                    response = requests.get(self.semantic_scholar_base, params=params, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    
                    is_valid = False
                    matched_paper = None
                    
                    if data and "data" in data and len(data["data"]) > 0:
                        # Check if any result is a good match
                        for result in data["data"]:
                            result_title = result.get("title", "").lower()
                            search_title = cleaned_title.lower()
                            
                            # Simple similarity check
                            search_words = set(search_title.split())
                            result_words = set(result_title.split())
                            
                            if len(search_words) > 0:
                                overlap = len(search_words.intersection(result_words))
                                similarity = overlap / len(search_words)
                                
                                if similarity > 0.3:  # 30% word overlap
                                    is_valid = True
                                    matched_paper = result
                                    break
                    
                    result_data = {
                        "reference": citation,
                        "valid": is_valid,
                        "searched_title": cleaned_title
                    }
                    
                    if matched_paper:
                        result_data["matched_paper"] = {
                            "title": matched_paper.get("title"),
                            "authors": matched_paper.get("authors", []),
                            "year": matched_paper.get("year"),
                            "venue": matched_paper.get("venue")
                        }
                        logger.info(f"Citation validated: {cleaned_title[:50]}... -> {matched_paper.get('title', '')[:50]}...")
                    else:
                        result_data["reason"] = "No matching paper found in Semantic Scholar"
                        logger.info(f"Citation not found: {cleaned_title[:50]}...")
                    
                    citation_results.append(result_data)
                    
                except requests.exceptions.RequestException as e:
                    logger.warning(f"Semantic Scholar API request failed for citation {i}: {e}")
                    citation_results.append({
                        "reference": citation,
                        "valid": False,
                        "reason": "API request failed",
                        "searched_title": cleaned_title
                    })
                    
            except Exception as e:
                logger.warning(f"Error validating citation {i}: {e}")
                citation_results.append({
                    "reference": citation,
                    "valid": False,
                    "reason": f"Processing error: {str(e)}"
                })
        
        return citation_results
    
    def get_citations_report(self, text):
        """Get comprehensive citations report"""
        citations = self.extract_citations(text)
        validated_citations = self.validate_citations(citations)
        
        total_citations = len(validated_citations)
        valid_citations = sum(1 for c in validated_citations if c['valid'])
        invalid_citations = total_citations - valid_citations
        
        return {
            "total_citations": total_citations,
            "valid_citations": valid_citations,
            "invalid_citations": invalid_citations,
            "citations": validated_citations,
            "quality_score": (valid_citations / total_citations * 100) if total_citations > 0 else 0,
            "recommendations": self._get_citation_recommendations(total_citations, valid_citations)
        }
    
    def _get_citation_recommendations(self, total, valid):
        """Get recommendations based on citation analysis"""
        if total == 0:
            return "No citations found. Consider adding references to support your claims."
        elif valid == 0:
            return "No valid citations found. Review reference formatting and accuracy."
        elif valid / total < 0.5:
            return "Less than 50% of citations are valid. Review and correct citation formatting."
        elif valid / total < 0.8:
            return "Most citations are valid, but some need correction."
        else:
            return "Citations appear to be well-formatted and accurate."

# Legacy functions for backward compatibility
_DOI_RE = re.compile(r'\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b', re.IGNORECASE)
_URL_RE = re.compile(r'https?://[^\s<>"\)]+', re.IGNORECASE)

# APA-like in-text (Author, 2017) or (Author & Author, 2019)
_APA_INTEXT_RE = re.compile(r'\(([A-Z][A-Za-z\-]+(?:\s*&\s*[A-Z][A-Za-z\-]+)?(?:,\s*[A-Z][A-Za-z\-]+)*)\s*,\s*(\d{4}[a-z]?)\)', re.UNICODE)
# Numeric in-text [12] or [1,2,3]
_NUM_INTEXT_RE = re.compile(r'\[(\d+(?:\s*,\s*\d+)*)\]')

_SECTION_HEAD_RE = re.compile(r'^\s*(references|bibliography|works\s+cited)\s*$', re.IGNORECASE)

# Semantic Scholar API is free and doesn't require API keys for basic usage
def _has_external_apis():
    """Semantic Scholar API is always available (no API key required)."""
    return True  # Semantic Scholar API is free and open

def _split_lines(text: str) -> List[str]:
    return [ln.strip() for ln in text.splitlines()]

def _find_references_block(lines: List[str]) -> List[str]:
    """Return lines that appear to belong to the references section."""
    refs_start = None
    for idx, ln in enumerate(lines):
        if _SECTION_HEAD_RE.match(ln):
            refs_start = idx + 1
            break
    if refs_start is None:
        return []

    # collect until next big ALLCAPS/numbered header or end
    block = []
    for ln in lines[refs_start:]:
        if ln.strip() == "":
            block.append(ln)
            continue
        # crude next-section detector
        if re.match(r'^[A-Z][A-Z0-9 ._-]{3,}$', ln) and len(ln.split()) <= 6:
            # Ex: APPENDIX A, RESULTS, SUPPLEMENT, etc.
            break
        block.append(ln)
    return block

def _chunk_references(ref_lines: List[str]) -> List[str]:
    """Group reference entries from lines (empty line or line starting with [n] splits)."""
    entries, buf = [], []
    for ln in ref_lines:
        if not ln or re.match(r'^\s*\[\d+\]\s+', ln):  # IEEE style numbered
            if buf:
                entries.append(" ".join(buf).strip())
                buf = []
            if ln and re.match(r'^\s*\[\d+\]\s+', ln):
                buf.append(ln)
        else:
            buf.append(ln)
    if buf:
        entries.append(" ".join(buf).strip())
    # filter short junk
    return [e for e in entries if len(e) > 20]

def _extract_title_guess(ref: str) -> str:
    """Very rough title guess: remove DOI/URL and try to grab quoted or between year and period."""
    cleaned = _DOI_RE.sub('', ref)
    cleaned = _URL_RE.sub('', cleaned)
    m = re.search(r'"([^"]+)"|"([^"]+)"', cleaned)
    if m:
        return (m.group(1) or m.group(2)).strip()

    # try: after year ... before next period
    y = re.search(r'\((\d{4}[a-z]?)\)\.?\s*(.+?)\.', cleaned)
    if y:
        return y.group(2).strip()
    # fallback: first longish segment
    parts = [p.strip() for p in re.split(r'\.\s+', cleaned) if len(p.strip()) > 5]
    return parts[1] if len(parts) > 1 else (parts[0] if parts else cleaned[:120])

def _validate_with_external_apis(citation_data: Dict) -> bool:
    """
    Validate citation using Semantic Scholar API (free, no key required).
    Returns True if valid, False otherwise.
    """
    try:
        title = citation_data.get("cleaned_title", "").strip()
        if not title or len(title) < 5:
            return False
        
        # Use Semantic Scholar API to search for the paper
        search_url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": title,
            "fields": "title,authors,year",
            "limit": 3
        }
        
        try:
            response = requests.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data and "data" in data and len(data["data"]) > 0:
                # Check if any result is a reasonable match
                for result in data["data"]:
                    result_title = result.get("title", "").lower()
                    search_title = title.lower()
                    
                    # Simple similarity check - if significant overlap in words
                    search_words = set(search_title.split())
                    result_words = set(result_title.split())
                    
                    if len(search_words) > 0:
                        overlap = len(search_words.intersection(result_words))
                        similarity = overlap / len(search_words)
                        
                        if similarity > 0.3:  # 30% word overlap
                            logger.info(f"Citation validated via Semantic Scholar: {title[:50]}...")
                            return True
            
            logger.info(f"Citation not found in Semantic Scholar: {title[:50]}...")
            return False
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Semantic Scholar API request failed: {e}")
            # Fall back to heuristic validation if API fails
            return bool(citation_data.get("doi") or citation_data.get("url"))
            
    except Exception as e:
        logger.warning(f"Error in external API validation: {e}")
        # Fall back to heuristic validation
        return bool(citation_data.get("doi") or citation_data.get("url"))

def validate(text: str) -> List[Dict]:
    """
    Parse in-text citations, DOIs/URLs, and the References section.
    Always returns a list of dicts: {raw, cleaned_title, doi, url, valid}
    
    This function is designed to work gracefully without external API keys.
    """
    try:
        if not text or not text.strip():
            logger.info("Empty text provided for citation validation")
            return []

        lines = _split_lines(text)
        refs_block = _find_references_block(lines)
        ref_entries = _chunk_references(refs_block) if refs_block else []

        results: List[Dict] = []

        # 1) Bibliography entries
        for ref in ref_entries:
            try:
                doi = None
                url = None
                mdoi = _DOI_RE.search(ref)
                if mdoi:
                    doi = mdoi.group(0)
                murl = _URL_RE.search(ref)
                if murl:
                    url = murl.group(0)
                title = _extract_title_guess(ref)
                
                citation_data = {
                    "raw": ref,
                    "cleaned_title": title,
                    "doi": doi,
                    "url": url,
                }
                
                # Use safe validation that handles missing APIs
                valid = _validate_with_external_apis(citation_data)
                citation_data["valid"] = valid
                
                results.append(citation_data)
            except Exception as e:
                logger.warning(f"Error processing bibliography entry: {e}")
                results.append({
                    "raw": ref,
                    "cleaned_title": "Processing error",
                    "doi": None,
                    "url": None,
                    "valid": False
                })

        # 2) In-text APA-style (Author, 2017)
        for m in _APA_INTEXT_RE.finditer(text):
            try:
                raw = m.group(0)
                results.append({
                    "raw": raw,
                    "cleaned_title": "",
                    "doi": None,
                    "url": None,
                    "valid": False  # In-text citations can't be validated without reference list
                })
            except Exception as e:
                logger.warning(f"Error processing APA citation: {e}")

        # 3) In-text numeric [1], [2,3]
        for m in _NUM_INTEXT_RE.finditer(text):
            try:
                raw = m.group(0)
                results.append({
                    "raw": raw,
                    "cleaned_title": "",
                    "doi": None,
                    "url": None,
                    "valid": False  # In-text citations can't be validated without reference list
                })
            except Exception as e:
                logger.warning(f"Error processing numeric citation: {e}")

        logger.info("Citations parsed: %d", len(results))
        return results
        
    except Exception as e:
        logger.error(f"Citation validation failed: {e}")
        # Return safe fallback
        return [{"reference": "Unknown", "valid": False}]
