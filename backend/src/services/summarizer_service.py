import re
import logging
import os
from flask import current_app
from transformers import pipeline

logger = logging.getLogger(__name__)

# Cache models in memory so they don't reload every request
_model_cache = {}

class SummarizerService:
    """Service for text summarization using transformers"""
    
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.model_name = model_name
        self.summarizer = None
    
    def get_summarizer(self):
        """Get or create summarizer instance with error handling"""
        if self.summarizer is None:
            try:
                logger.info("Loading summarizer model...")
                self.summarizer = pipeline("summarization", model=self.model_name)
                logger.info("Summarizer model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load summarizer: {e}")
                # Return a fallback function
                def fallback_summarizer(text, **kwargs):
                    # Simple extractive summarization fallback
                    sentences = text.split('.')[:3]
                    return [{"summary_text": '. '.join(sentences) + '.'}]
                self.summarizer = fallback_summarizer
        return self.summarizer
    
    def summarize_text(self, text, max_length=200, min_length=50):
        """Summarize text with error handling"""
        try:
            summarizer_model = self.get_summarizer()
            
            # Limit text for summarization to avoid memory issues
            if len(text) > 1024:
                text_for_summary = text[:1024]
                logger.info(f"Text truncated to {len(text_for_summary)} characters for summarization")
            else:
                text_for_summary = text
            
            # Generate summary
            summary_result = summarizer_model(
                text_for_summary, 
                max_length=max_length, 
                min_length=min_length, 
                do_sample=False
            )
            
            if isinstance(summary_result, list) and len(summary_result) > 0:
                return summary_result[0]["summary_text"]
            else:
                return summary_result["summary_text"]
                
        except Exception as e:
            logger.warning(f"Summarization failed: {e}")
            # Fallback: use first few sentences
            sentences = text.split('.')[:3]
            return '. '.join(sentences) + '.'
    
    def get_summary_with_stats(self, text):
        """Get summary with additional statistics"""
        summary = self.summarize_text(text)
        
        original_word_count = len(text.split())
        summary_word_count = len(summary.split())
        compression_ratio = (original_word_count - summary_word_count) / original_word_count * 100
        
        return {
            "summary": summary,
            "original_length": original_word_count,
            "summary_length": summary_word_count,
            "compression_ratio": round(compression_ratio, 2)
        }
    
    def summarize_by_sections(self, text, section_length=500):
        """Summarize text by breaking it into sections"""
        words = text.split()
        sections = []
        
        # Break text into sections
        for i in range(0, len(words), section_length):
            section = ' '.join(words[i:i + section_length])
            if len(section) > 50:  # Only process sections with meaningful content
                sections.append(section)
        
        # Summarize each section
        section_summaries = []
        for i, section in enumerate(sections):
            try:
                summary = self.summarize_text(section, max_length=100, min_length=20)
                section_summaries.append({
                    "section": i + 1,
                    "summary": summary
                })
            except Exception as e:
                logger.warning(f"Failed to summarize section {i + 1}: {e}")
                continue
        
        # Combine section summaries
        combined_summary = ' '.join([s["summary"] for s in section_summaries])
        
        return {
            "sections": section_summaries,
            "combined_summary": combined_summary,
            "total_sections": len(section_summaries)
        }

# Legacy functions for backward compatibility
def summarize_text(text: str) -> str:
    """Summarize text (shortcut for direct calls)."""
    if not text or len(text.strip()) < 100:
        return text.strip()
    try:
        return _summarize_with_hf(text)
    except Exception as e:
        logging.error(f"HF summarization failed, fallback to heuristic: {e}")
        return _summarize_heuristic(text)

def summarize(text: str, use_hf: bool = True) -> str:
    """Summarize text using HuggingFace transformers or fallback heuristic."""
    if not text or len(text.strip()) < 100:
        return "Document too short to summarize effectively."
    
    use_hf_config = current_app.config.get('USE_HF_SUMMARIZER', True) if current_app else True
    
    if use_hf and use_hf_config:
        try:
            return _summarize_with_hf(text)
        except Exception as e:
            logging.error(f"HF summarization failed, fallback to heuristic: {e}")
            return _summarize_heuristic(text)
    else:
        return _summarize_heuristic(text)

def _get_summarizer():
    """Load and cache HuggingFace summarizer."""
    if 'summarizer' not in _model_cache:
        try:
            model_name = current_app.config.get('HF_MODEL_NAME', 'facebook/bart-large-cnn') if current_app else 'facebook/bart-large-cnn'
            cache_dir = current_app.config.get('HF_CACHE_DIR', './models_cache') if current_app else './models_cache'
            os.makedirs(cache_dir, exist_ok=True)
            
            logging.info(f"Loading HuggingFace model: {model_name}")
            _model_cache['summarizer'] = pipeline(
                "summarization",
                model=model_name,
                cache_dir=cache_dir,
                device=-1,  # -1 for CPU, 0 for GPU
                framework="pt"
            )
            logging.info("HuggingFace summarizer loaded successfully.")
        except ImportError as e:
            raise Exception(f"transformers library not installed: {e}")
        except Exception as e:
            raise Exception(f"Failed to load HuggingFace model: {e}")
    
    return _model_cache['summarizer']

def _summarize_with_hf(text: str) -> str:
    """Summarize using HuggingFace model with chunking and truncation."""
    summarizer = _get_summarizer()
    text = text.strip()
    
    if len(text) < 100:
        return text

    # Limit chunk size for BART (~1024 tokens ≈ 1200–1500 chars)
    chunk_size = 1000
    chunks = []

    if len(text) <= chunk_size:
        chunks = [text]
    else:
        paragraphs = text.split('\n\n')
        current_chunk = ""
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) <= chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
        if current_chunk:
            chunks.append(current_chunk.strip())

    summaries = []
    for chunk in chunks:
        if len(chunk.strip()) < 50:
            continue
        try:
            summary = summarizer(
                chunk,
                max_length=150,
                min_length=50,
                truncation=True,
                do_sample=False
            )[0]['summary_text']
            summaries.append(summary.strip())
        except Exception as e:
            logging.warning(f"Chunk summarization failed: {e}")
            continue

    if not summaries:
        raise Exception("No summaries generated from any chunk.")

    final_summary = ' '.join(summaries)

    # If combined summary too long, summarize it again
    if len(final_summary.split()) > 250:
        try:
            final_summary = summarizer(
                final_summary,
                max_length=200,
                min_length=100,
                truncation=True,
                do_sample=False
            )[0]['summary_text']
        except Exception as e:
            logging.warning(f"Failed to re-summarize combined text: {e}")
            final_summary = ' '.join(final_summary.split()[:200])

    return final_summary.strip()

def _summarize_heuristic(text: str) -> str:
    """Fallback: pick important sentences."""
    sentences = _split_into_sentences(text)
    important_keywords = [
        'study', 'result', 'method', 'conclude', 'finding', 'research',
        'analysis', 'experiment', 'data', 'significant', 'demonstrate',
        'propose', 'novel', 'approach', 'framework', 'model', 'algorithm'
    ]
    sentence_scores = []
    for sentence in sentences:
        if len(sentence.split()) < 5:
            continue
        score = 0
        s_lower = sentence.lower()
        word_count = len(sentence.split())
        if 15 <= word_count <= 30:
            score += 2
        elif 10 <= word_count <= 40:
            score += 1
        for keyword in important_keywords:
            if keyword in s_lower:
                score += 1
        idx = sentences.index(sentence)
        if idx < len(sentences) * 0.2 or idx > len(sentences) * 0.8:
            score += 1
        sentence_scores.append((sentence, score))
    
    sentence_scores.sort(key=lambda x: x[1], reverse=True)
    selected = []
    total_words = 0
    for sentence, score in sentence_scores:
        if total_words + len(sentence.split()) <= 200:
            selected.append(sentence)
            total_words += len(sentence.split())
        if len(selected) >= 7 or total_words >= 180:
            break
    if not selected:
        selected = sentences[:3]
    return ' '.join([s for s in sentences if s in selected])

def _split_into_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 10]
