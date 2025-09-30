import re
import logging
from typing import Dict, List, Tuple
import json
import statistics

logger = logging.getLogger(__name__)

class CritiqueService:
    """Advanced service for comprehensive academic paper critique"""
    
    def __init__(self):
        # Enhanced methodology assessment keywords
        self.methodology_frameworks = {
            "experimental": ["experiment", "trial", "randomized", "control group", "treatment", "intervention"],
            "survey": ["survey", "questionnaire", "cross-sectional", "longitudinal", "cohort"],
            "qualitative": ["interview", "focus group", "ethnography", "case study", "grounded theory", "thematic analysis"],
            "quantitative": ["statistical", "regression", "correlation", "anova", "t-test", "chi-square"],
            "mixed_methods": ["mixed methods", "triangulation", "concurrent", "sequential"],
            "systematic_review": ["systematic review", "meta-analysis", "literature review", "scoping review"]
        }
        
        # Statistical validity indicators
        self.statistical_terms = {
            "sample_size": ["sample size", "power analysis", "n =", "participants", "subjects"],
            "significance": ["p-value", "p <", "significant", "alpha", "confidence interval"],
            "effect_size": ["effect size", "cohen's d", "eta squared", "r squared", "odds ratio"],
            "assumptions": ["normality", "homogeneity", "independence", "linearity", "assumptions"]
        }
        
        # Argument evaluation patterns
        self.argument_patterns = {
            "strong_claims": ["proves", "demonstrates", "confirms", "establishes", "validates"],
            "weak_claims": ["suggests", "indicates", "implies", "appears", "seems", "may indicate"],
            "causal_language": ["causes", "results in", "leads to", "due to", "because of"],
            "correlation_language": ["associated with", "related to", "correlated", "linked to"]
        }
        
        # Bias detection patterns
        self.bias_indicators = {
            "selection_bias": ["convenience sample", "voluntary", "self-selected", "opted in"],
            "confirmation_bias": ["as expected", "predictably", "obviously", "naturally"],
            "publication_bias": ["negative results", "null findings", "non-significant"],
            "reporting_bias": ["data not shown", "results omitted", "selective reporting"]
        }
        
        # Academic rigor indicators
        self.rigor_indicators = {
            "transparency": ["data available", "code available", "supplementary", "appendix"],
            "reproducibility": ["reproducible", "replicable", "open science", "pre-registered"],
            "peer_review": ["peer reviewed", "blind review", "reviewer comments"],
            "ethics": ["ethics approval", "institutional review", "consent", "anonymized"]
        }
        
        # Legacy compatibility attributes
        self.methodology_keywords = [kw for keywords in self.methodology_frameworks.values() for kw in keywords]
        self.bias_terms = self.bias_indicators["confirmation_bias"] + ["clearly", "obviously", "undoubtedly"]
        self.academic_red_flags = self.argument_patterns["strong_claims"] + ["always", "never", "all", "none"]

    def critique_paper(self, text):
        """Priority 1 & 2: Real academic analysis with comprehensive critique features"""
        try:
            critique_result = {}
            
            # Priority 1: Real academic analysis
            methodology_analysis = self._analyze_methodology_advanced(text)
            critique_result.update(methodology_analysis)
            
            argument_analysis = self._evaluate_arguments_advanced(text)
            critique_result.update(argument_analysis)
            
            # Priority 2: Comprehensive critique features
            bias_analysis = self._detect_bias_comprehensive(text)
            critique_result.update(bias_analysis)
            
            validity_analysis = self._assess_validity_comprehensive(text)
            critique_result.update(validity_analysis)
            
            # Enhanced overall assessment
            critique_result["overall_assessment"] = self._calculate_comprehensive_score(critique_result)
            critique_result["academic_recommendations"] = self._generate_academic_recommendations(critique_result)
            critique_result["quality_grade"] = self._assign_academic_grade(critique_result)
            
            return critique_result
            
        except Exception as e:
            logger.error(f"Error in academic critique: {e}")
            return {"error": "Analysis failed", "suggestion": "Check paper format and content"}
    
    def _analyze_methodology_advanced(self, text):
        """Priority 1: Real methodology assessment with framework detection"""
        text_lower = text.lower()
        
        # Detect research frameworks
        detected_frameworks = []
        framework_scores = {}
        
        for framework, keywords in self.methodology_frameworks.items():
            found = [kw for kw in keywords if kw in text_lower]
            if found:
                detected_frameworks.append(framework)
                framework_scores[framework] = {
                    "keywords_found": found,
                    "strength": len(found) * 20
                }
        
        # Sample size analysis
        sample_patterns = [r'n\s*=\s*(\d+)', r'sample size.*?(\d+)', r'(\d+)\s+participants']
        sample_sizes = []
        for pattern in sample_patterns:
            matches = re.findall(pattern, text_lower)
            sample_sizes.extend([int(m) for m in matches if m.isdigit()])
        
        # Statistical rigor check
        stats_found = []
        for category, terms in self.statistical_terms.items():
            found = [term for term in terms if term in text_lower]
            if found:
                stats_found.extend(found)
        
        methodology_score = min(100, len(detected_frameworks) * 25 + len(stats_found) * 5)
        
        return {
            "methodology_frameworks_detected": detected_frameworks,
            "framework_analysis": framework_scores,
            "sample_size_analysis": {"sizes_found": sample_sizes, "adequate": max(sample_sizes) > 30 if sample_sizes else False},
            "statistical_rigor": {"terms_found": stats_found, "count": len(stats_found)},
            "methodology_quality_score": methodology_score
        }
    
    def _evaluate_arguments_advanced(self, text):
        """Priority 1: Advanced argument evaluation and logical reasoning assessment"""
        text_lower = text.lower()
        
        # Analyze claim strength
        claim_analysis = {}
        for claim_type, patterns in self.argument_patterns.items():
            found = [p for p in patterns if p in text_lower]
            if found:
                claim_analysis[claim_type] = {"patterns_found": found, "count": len(found)}
        
        # Evidence-to-claim ratio analysis
        evidence_keywords = ["data", "evidence", "results", "findings", "analysis", "study", "research"]
        evidence_count = sum(text_lower.count(word) for word in evidence_keywords)
        
        strong_claims = len(claim_analysis.get("strong_claims", {}).get("patterns_found", []))
        claim_support_ratio = evidence_count / max(strong_claims, 1)
        
        # Logical flow assessment
        logical_connectors = ["therefore", "thus", "consequently", "because", "since", "as a result"]
        logical_flow_count = sum(text_lower.count(word) for word in logical_connectors)
        
        argument_score = min(100, claim_support_ratio * 10 + logical_flow_count * 5)
        
        return {
            "claim_strength_analysis": claim_analysis,
            "evidence_support_ratio": round(claim_support_ratio, 2),
            "logical_flow_indicators": logical_flow_count,
            "argument_quality_score": round(argument_score, 1)
        }
    
    def _detect_bias_comprehensive(self, text):
        """Priority 2: Comprehensive bias detection across multiple dimensions"""
        text_lower = text.lower()
        
        # Multi-dimensional bias analysis
        bias_detection = {}
        overall_bias_score = 100
        
        for bias_type, indicators in self.bias_indicators.items():
            found = [indicator for indicator in indicators if indicator in text_lower]
            if found:
                severity = "High" if len(found) > 2 else "Medium" if len(found) > 1 else "Low"
                bias_detection[bias_type] = {
                    "indicators_found": found,
                    "severity": severity,
                    "impact_score": len(found) * 15
                }
                overall_bias_score -= len(found) * 10
        
        # Language objectivity analysis
        subjective_terms = ["obviously", "clearly", "undoubtedly", "certainly", "definitely"]
        objective_terms = ["suggests", "indicates", "appears", "may", "could", "possibly"]
        
        subjective_count = sum(text_lower.count(term) for term in subjective_terms)
        objective_count = sum(text_lower.count(term) for term in objective_terms)
        
        objectivity_ratio = objective_count / max(subjective_count + objective_count, 1)
        
        # Statistical bias indicators
        stat_bias_indicators = ["cherry-picking", "p-hacking", "data dredging", "selective reporting"]
        stat_bias_found = [term for term in stat_bias_indicators if term in text_lower]
        
        bias_risk = "Low" if overall_bias_score > 80 else "Medium" if overall_bias_score > 60 else "High"
        
        return {
            "bias_types_analysis": bias_detection,
            "language_objectivity": {"ratio": round(objectivity_ratio, 2), "assessment": "Good" if objectivity_ratio > 0.6 else "Needs improvement"},
            "statistical_bias_indicators": stat_bias_found,
            "overall_bias_risk": bias_risk,
            "bias_score": max(0, overall_bias_score)
        }
    
    def _assess_validity_comprehensive(self, text):
        """Priority 2: Comprehensive validity assessment (internal, external, construct, statistical)"""
        text_lower = text.lower()
        
        validity_scores = {}
        
        # Internal validity assessment
        internal_indicators = ["control group", "randomization", "blinding", "confounding variables"]
        internal_found = [term for term in internal_indicators if term in text_lower]
        validity_scores["internal_validity"] = {
            "indicators_found": internal_found,
            "score": len(internal_found) * 25,
            "assessment": "Strong" if len(internal_found) > 2 else "Moderate" if len(internal_found) > 0 else "Weak"
        }
        
        # External validity assessment
        external_indicators = ["generalizability", "population", "representative sample", "external validity"]
        external_found = [term for term in external_indicators if term in text_lower]
        validity_scores["external_validity"] = {
            "indicators_found": external_found,
            "score": len(external_found) * 25,
            "assessment": "Strong" if len(external_found) > 2 else "Moderate" if len(external_found) > 0 else "Weak"
        }
        
        # Construct validity assessment
        construct_indicators = ["validity", "measurement", "instrument", "reliable", "correlation"]
        construct_found = [term for term in construct_indicators if term in text_lower]
        validity_scores["construct_validity"] = {
            "indicators_found": construct_found,
            "score": len(construct_found) * 20,
            "assessment": "Strong" if len(construct_found) > 3 else "Moderate" if len(construct_found) > 1 else "Weak"
        }
        
        # Statistical conclusion validity
        statistical_indicators = ["power analysis", "effect size", "confidence interval", "significance level"]
        statistical_found = [term for term in statistical_indicators if term in text_lower]
        validity_scores["statistical_validity"] = {
            "indicators_found": statistical_found,
            "score": len(statistical_found) * 25,
            "assessment": "Strong" if len(statistical_found) > 2 else "Moderate" if len(statistical_found) > 0 else "Weak"
        }
        
        # Overall validity score
        total_score = sum(v["score"] for v in validity_scores.values())
        overall_validity = min(100, total_score / 4)
        
        return {
            "validity_analysis": validity_scores,
            "overall_validity_score": round(overall_validity, 1),
            "validity_grade": "A" if overall_validity > 80 else "B" if overall_validity > 60 else "C" if overall_validity > 40 else "D"
        }
    
    def _calculate_comprehensive_score(self, results):
        """Calculate weighted comprehensive academic quality score"""
        methodology_score = results.get("methodology_quality_score", 0)
        argument_score = results.get("argument_quality_score", 0)
        bias_score = results.get("bias_score", 100)
        validity_score = results.get("overall_validity_score", 0)
        
        # Weighted scoring (methodology and arguments are most important)
        weighted_score = (
            methodology_score * 0.35 +
            argument_score * 0.35 + 
            bias_score * 0.15 +
            validity_score * 0.15
        )
        
        return {
            "overall_score": round(weighted_score, 1),
            "grade": "A" if weighted_score > 85 else "B" if weighted_score > 70 else "C" if weighted_score > 55 else "D" if weighted_score > 40 else "F",
            "category": "Excellent" if weighted_score > 85 else "Good" if weighted_score > 70 else "Acceptable" if weighted_score > 55 else "Needs Improvement"
        }
    
    def _generate_academic_recommendations(self, results):
        """Generate specific academic improvement recommendations"""
        recommendations = []
        
        # Methodology recommendations
        if not results.get("methodology_frameworks_detected"):
            recommendations.append("Clearly specify your research methodology framework (experimental, survey, qualitative, etc.)")
        
        if results.get("methodology_quality_score", 0) < 50:
            recommendations.append("Enhance methodology section with detailed procedures, sample size justification, and statistical approach")
        
        # Argument evaluation recommendations
        if results.get("argument_quality_score", 0) < 50:
            recommendations.append("Strengthen arguments with more evidence support and clearer logical connections")
        
        if results.get("evidence_support_ratio", 0) < 3:
            recommendations.append("Provide more empirical evidence to support your claims and conclusions")
        
        # Bias reduction recommendations
        if results.get("overall_bias_risk") == "High":
            recommendations.append("Reduce subjective language and acknowledge potential biases and limitations")
        
        # Validity improvement recommendations
        validity_grade = results.get("validity_grade", "D")
        if validity_grade in ["C", "D"]:
            recommendations.append("Address validity concerns by discussing internal/external validity and measurement reliability")
        
        return recommendations[:6]  # Limit to top 6 recommendations
    
    def _assign_academic_grade(self, results):
        """Assign overall academic quality grade with detailed breakdown"""
        overall_score = results.get("overall_assessment", {}).get("overall_score", 0)
        
        if overall_score >= 90:
            return {"grade": "A+", "description": "Outstanding academic quality"}
        elif overall_score >= 85:
            return {"grade": "A", "description": "Excellent academic standards"}
        elif overall_score >= 80:
            return {"grade": "A-", "description": "Very good quality"}
        elif overall_score >= 75:
            return {"grade": "B+", "description": "Good academic work"}
        elif overall_score >= 70:
            return {"grade": "B", "description": "Satisfactory quality"}
        elif overall_score >= 65:
            return {"grade": "B-", "description": "Below average, needs improvement"}
        elif overall_score >= 60:
            return {"grade": "C+", "description": "Marginal quality"}
        elif overall_score >= 55:
            return {"grade": "C", "description": "Poor quality, significant issues"}
        else:
            return {"grade": "F", "description": "Fails academic standards"}
        """Analyze methodology section"""
        text_lower = text.lower()
        found_keywords = [kw for kw in self.methodology_keywords if kw in text_lower]
        
        methodology_score = min(100, len(found_keywords) * 10)  # Max 100
        
        if not found_keywords:
            return {
                "methodology_issues": "No standard research methodology terms found.",
                "methodology_score": 0,
                "found_methodology_terms": []
            }
        else:
            return {
                "methodology_issues": f"Methodology terms found: {', '.join(found_keywords[:5])}.",
                "methodology_score": methodology_score,
                "found_methodology_terms": found_keywords
            }
    
    def _analyze_bias_language(self, text):
        """Analyze bias language"""
        text_lower = text.lower()
        found_bias = [term for term in self.bias_terms if term in text_lower]
        
        bias_score = max(0, 100 - len(found_bias) * 15)  # Deduct points for bias
        
        return {
            "bias_language": found_bias[:5] if found_bias else [],
            "bias_score": bias_score,
            "bias_severity": "High" if len(found_bias) > 3 else "Medium" if len(found_bias) > 1 else "Low"
        }
    
    def _analyze_academic_rigor(self, text):
        """Analyze academic rigor"""
        text_lower = text.lower()
        found_red_flags = [term for term in self.academic_red_flags if term in text_lower]
        
        rigor_score = max(0, 100 - len(found_red_flags) * 10)
        
        return {
            "academic_red_flags": found_red_flags[:5] if found_red_flags else [],
            "rigor_score": rigor_score,
            "rigor_assessment": "Needs improvement" if rigor_score < 70 else "Acceptable" if rigor_score < 90 else "Good"
        }
    
    def _analyze_structure(self, text):
        """Analyze paper structure"""
        text_lower = text.lower()
        
        # Look for common academic sections
        sections = {
            "abstract": "abstract" in text_lower,
            "introduction": "introduction" in text_lower,
            "methodology": any(term in text_lower for term in ["methodology", "methods", "approach"]),
            "results": "results" in text_lower,
            "discussion": "discussion" in text_lower,
            "conclusion": "conclusion" in text_lower,
            "references": any(term in text_lower for term in ["references", "bibliography"])
        }
        
        structure_score = sum(1 for present in sections.values() if present) * 14  # ~14 points per section
        
        return {
            "structure_analysis": sections,
            "structure_score": min(100, structure_score),
            "missing_sections": [section for section, present in sections.items() if not present]
        }
    
    def _calculate_overall_score(self, critique_result):
        """Calculate overall quality score"""
        methodology_score = critique_result.get("methodology_score", 0)
        bias_score = critique_result.get("bias_score", 100)
        rigor_score = critique_result.get("rigor_score", 100)
        structure_score = critique_result.get("structure_score", 0)
        
        # Weighted average
        overall_score = (
            methodology_score * 0.3 +
            bias_score * 0.3 +
            rigor_score * 0.2 +
            structure_score * 0.2
        )
        
        return round(overall_score, 1)
    
    def _generate_recommendations(self, critique_result):
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if critique_result.get("methodology_score", 0) < 30:
            recommendations.append("Consider describing your research methods in more detail.")
        
        if critique_result.get("bias_language"):
            recommendations.append("Avoid subjective language to maintain objectivity.")
        
        if critique_result.get("academic_red_flags"):
            recommendations.append("Use more precise and qualified language instead of absolute statements.")
        
        missing_sections = critique_result.get("missing_sections", [])
        if missing_sections:
            recommendations.append(f"Consider adding the following sections: {', '.join(missing_sections[:3])}.")
        
        if not recommendations:
            recommendations.append("The paper appears to follow good academic practices.")
        
        return recommendations
    
    def count_words(self, text):
        """Count words in text"""
        try:
            words = re.findall(r'\b\w+\b', text)
            return len(words)
        except:
            return 0
    
    def get_readability_metrics(self, text):
        """Get basic readability metrics"""
        try:
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            words = re.findall(r'\b\w+\b', text)
            
            if not sentences or not words:
                return {"avg_sentence_length": 0, "total_sentences": 0, "total_words": 0}
            
            avg_sentence_length = len(words) / len(sentences)
            
            return {
                "avg_sentence_length": round(avg_sentence_length, 1),
                "total_sentences": len(sentences),
                "total_words": len(words),
                "readability_assessment": self._assess_readability(avg_sentence_length)
            }
        except Exception as e:
            logger.warning(f"Error calculating readability metrics: {e}")
            return {"avg_sentence_length": 0, "total_sentences": 0, "total_words": 0}
    
    def _assess_readability(self, avg_sentence_length):
        """Assess readability based on average sentence length"""
        if avg_sentence_length < 15:
            return "Easy to read"
        elif avg_sentence_length < 25:
            return "Moderate complexity"
        else:
            return "Complex - consider shorter sentences"

# Legacy functions for backward compatibility
def critique_paper(text: str) -> dict:
    """Critique paper using basic NLP and heuristics."""
    service = CritiqueService()
    return service.critique_paper(text)
    """
    Critique paper using basic NLP and heuristics.
    
    Args:
        text: Full document text
        
    Returns:
        Dictionary with clarity, methodology, bias, and structure assessments
    """
    text_lower = text.lower()
    
    critique_result = {
        "clarity": _assess_clarity(text, text_lower),
        "methodology": _assess_methodology(text_lower),
        "bias": _assess_bias(text_lower),
        "structure": _assess_structure(text, text_lower)
    }
    
    return critique_result

def _assess_clarity(text: str, text_lower: str) -> str:
    """Assess writing clarity and readability."""
    issues = []
    
    # Sentence length analysis
    sentences = re.split(r'[.!?]+', text)
    sentence_lengths = [len(sentence.split()) for sentence in sentences if len(sentence.strip()) > 5]
    
    if sentence_lengths:
        avg_length = sum(sentence_lengths) / len(sentence_lengths)
        if avg_length > 25:
            issues.append("sentences too long")
        elif avg_length < 8:
            issues.append("sentences too short")
    
    # Check for jargon
    jargon_indicators = [
        'aforementioned', 'heretofore', 'wherein', 'whereby', 'thereof',
        'utilize', 'facilitate', 'implement', 'methodology'
    ]
    
    jargon_count = sum(text_lower.count(word) for word in jargon_indicators)
    if jargon_count > 15:
        issues.append("excessive jargon")
    
    # Check for definitions
    definition_indicators = ['defined as', 'refers to', 'means', 'is the', 'called']
    definition_count = sum(text_lower.count(phrase) for phrase in definition_indicators)
    if definition_count < 3 and len(text.split()) > 1000:
        issues.append("lacks definitions")
    
    if not issues:
        return "Good explanation with clear language"
    else:
        return f"Issues found: {', '.join(issues)}"

def _assess_methodology(text_lower: str) -> str:
    """Assess methodology description."""
    methodology_terms = [
        'method', 'methodology', 'approach', 'procedure', 'technique',
        'experiment', 'survey', 'interview', 'analysis', 'statistical'
    ]
    
    found_terms = [term for term in methodology_terms if term in text_lower]
    
    # Check for statistical methods
    stats_terms = [
        'p-value', 'significant', 'correlation', 'regression',
        'anova', 't-test', 'chi-square', 'confidence interval'
    ]
    
    found_stats = [term for term in stats_terms if term in text_lower]
    
    if len(found_terms) < 3:
        return "Methodology not clearly described"
    elif len(found_stats) == 0 and any(term in text_lower for term in ['quantitative', 'statistical', 'data']):
        return "Statistical methods not clearly described"
    else:
        return "Methodology adequately described"

def _assess_bias(text_lower: str) -> str:
    """Assess potential bias in the paper."""
    bias_indicators = [
        'obviously', 'clearly', 'undoubtedly', 'certainly', 'definitely',
        'always', 'never', 'all', 'none', 'everyone', 'no one'
    ]
    
    strong_claims = sum(text_lower.count(word) for word in bias_indicators)
    
    # Check for hedging language (good for reducing bias)
    hedge_words = [
        'might', 'could', 'may', 'possibly', 'perhaps', 'seems to',
        'appears to', 'suggests that', 'indicates that'
    ]
    
    hedge_count = sum(text_lower.count(word) for word in hedge_words)
    
    if strong_claims > hedge_count * 2:
        return "Potential bias detected - strong claims without hedging"
    elif 'limitation' in text_lower and 'bias' in text_lower:
        return "Bias considerations addressed"
    else:
        return "No apparent bias"

def _assess_structure(text: str, text_lower: str) -> str:
    """Assess document structure and organization."""
    # Check for common academic sections
    sections = {
        'abstract': ['abstract'],
        'introduction': ['introduction'],
        'methodology': ['method', 'methodology'],
        'results': ['result', 'findings'],
        'discussion': ['discussion', 'conclusion'],
        'references': ['references', 'bibliography']
    }
    
    found_sections = []
    for section_name, keywords in sections.items():
        if any(keyword in text_lower for keyword in keywords):
            found_sections.append(section_name)
    
    if len(found_sections) >= 4:
        return "Well organized with clear sections"
    elif len(found_sections) >= 2:
        return "Adequately organized but could improve structure"
    else:
        return "Poor organization - lacks clear sections"

def critique(text: str, summary: str) -> dict:
    """
    Perform heuristic critique of research paper.
    
    Args:
        text: Full document text
        summary: Document summary
    
    Returns:
        Dictionary with methodology, writing_flags, limitations, suggestions
    """
    text_lower = text.lower()
    summary_lower = summary.lower()
    
    critique_result = {
        "methodology": [],
        "writing_flags": [],
        "limitations": [],
        "suggestions": []
    }
    
    # Methodology analysis
    methodology_issues = _analyze_methodology(text_lower)
    critique_result["methodology"].extend(methodology_issues)
    
    # Writing and clarity analysis
    writing_issues = _analyze_writing_quality(text)
    critique_result["writing_flags"].extend(writing_issues)
    
    # Limitations analysis
    limitations = _analyze_limitations(text_lower)
    critique_result["limitations"].extend(limitations)
    
    # Generate suggestions
    suggestions = _generate_suggestions(text_lower, critique_result)
    critique_result["suggestions"].extend(suggestions)
    
    return critique_result

def _analyze_methodology(text: str) -> List[str]:
    """Analyze methodology aspects of the paper."""
    issues = []
    
    # Check for methodology terms
    methodology_terms = {
        'experiment': ['experiment', 'experimental', 'trial'],
        'survey': ['survey', 'questionnaire', 'poll'],
        'interview': ['interview', 'interviews', 'interviewed'],
        'qualitative': ['qualitative', 'thematic analysis', 'grounded theory'],
        'quantitative': ['quantitative', 'statistical', 'numerical'],
        'sample_size': ['sample size', 'n =', 'participants', 'subjects'],
        'randomized': ['randomized', 'random assignment', 'control group'],
        'bias': ['bias', 'confounding', 'threats to validity']
    }
    
    found_terms = {}
    for category, terms in methodology_terms.items():
        found = [term for term in terms if term in text]
        if found:
            found_terms[category] = found
    
    if found_terms:
        issues.append(f"Methodology terms found: {', '.join(found_terms.keys())}")
    else:
        issues.append("Limited methodology terminology detected")
    
    # Check for sample size mentions
    sample_patterns = [
        r'n\s*=\s*(\d+)',
        r'sample size.*?(\d+)',
        r'(\d+)\s+participants',
        r'(\d+)\s+subjects'
    ]
    
    sample_sizes = []
    for pattern in sample_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        sample_sizes.extend(matches)
    
    if sample_sizes:
        sizes = [int(s) for s in sample_sizes if s.isdigit()]
        if sizes:
            max_size = max(sizes)
            if max_size < 30:
                issues.append(f"Small sample size detected (n={max_size})")
            else:
                issues.append(f"Sample size mentioned (n={max_size})")
    else:
        issues.append("No explicit sample size found")
    
    # Check for statistical analysis
    stats_terms = [
        'p-value', 'p <', 'significant', 'correlation', 'regression',
        'anova', 't-test', 'chi-square', 'effect size', 'confidence interval'
    ]
    
    found_stats = [term for term in stats_terms if term in text]
    if found_stats:
        issues.append(f"Statistical analysis: {', '.join(found_stats[:3])}")
    else:
        issues.append("Limited statistical analysis terminology")
    
    return issues

def _analyze_writing_quality(text: str) -> List[str]:
    """Analyze writing quality and clarity."""
    issues = []
    
    # Sentence length analysis
    sentences = re.split(r'[.!?]+', text)
    sentence_lengths = [len(sentence.split()) for sentence in sentences if len(sentence.strip()) > 5]
    
    if sentence_lengths:
        avg_length = sum(sentence_lengths) / len(sentence_lengths)
        if avg_length > 25:
            issues.append(f"Long average sentence length ({avg_length:.1f} words)")
        elif avg_length < 10:
            issues.append(f"Short average sentence length ({avg_length:.1f} words)")
    
    # Passive voice detection (heuristic)
    passive_indicators = [
        r'\bwas\s+\w+ed\b',
        r'\bwere\s+\w+ed\b',
        r'\bbeen\s+\w+ed\b',
        r'\bis\s+\w+ed\b',
        r'\bare\s+\w+ed\b'
    ]
    
    passive_count = 0
    for pattern in passive_indicators:
        passive_count += len(re.findall(pattern, text, re.IGNORECASE))
    
    total_sentences = len([s for s in sentences if len(s.strip()) > 5])
    if total_sentences > 0:
        passive_ratio = passive_count / total_sentences
        if passive_ratio > 0.3:
            issues.append(f"High passive voice usage ({passive_ratio:.1%})")
    
    # Check for hedging language
    hedge_words = [
        'might', 'could', 'may', 'possibly', 'perhaps', 'seems to',
        'appears to', 'suggests that', 'indicates that'
    ]
    
    hedge_count = sum(text.lower().count(word) for word in hedge_words)
    if hedge_count > len(text.split()) * 0.02:  # More than 2% hedging
        issues.append("Frequent hedging language detected")
    
    # Check for clarity issues
    jargon_indicators = [
        'aforementioned', 'heretofore', 'wherein', 'whereby', 'thereof',
        'utilize', 'facilitate', 'implement', 'methodology'
    ]
    
    jargon_count = sum(text.lower().count(word) for word in jargon_indicators)
    if jargon_count > 10:
        issues.append("Academic jargon may affect readability")
    
    return issues

def _analyze_limitations(text: str) -> List[str]:
    """Analyze research limitations and validity threats."""
    limitations = []
    
    # Check for limitations section
    limitations_keywords = [
        'limitation', 'limitations', 'threats to validity',
        'scope', 'boundary', 'constraint', 'restriction'
    ]
    
    found_limitations = [kw for kw in limitations_keywords if kw in text]
    if found_limitations:
        limitations.append("Limitations section present")
    else:
        limitations.append("No explicit limitations discussion found")
    
    # Check for generalizability discussion
    generalizability_terms = [
        'generaliz', 'external validity', 'broader population',
        'applicability', 'transferability'
    ]
    
    if any(term in text for term in generalizability_terms):
        limitations.append("Generalizability addressed")
    else:
        limitations.append("Limited discussion of generalizability")
    
    # Check for data availability
    data_terms = [
        'data available', 'dataset', 'code available', 'reproducible',
        'replication', 'open data', 'github', 'repository'
    ]
    
    if any(term in text for term in data_terms):
        limitations.append("Data/code availability mentioned")
    else:
        limitations.append("No mention of data or code availability")
    
    # Check for ethical considerations
    ethics_terms = [
        'ethics', 'ethical', 'consent', 'irb', 'institutional review',
        'privacy', 'confidentiality', 'anonymous'
    ]
    
    if any(term in text for term in ethics_terms):
        limitations.append("Ethical considerations addressed")
    else:
        limitations.append("Limited ethical considerations discussion")
    
    return limitations

def _generate_suggestions(text: str, critique_result: dict) -> List[str]:
    """Generate improvement suggestions based on analysis."""
    suggestions = []
    
    # Methodology suggestions
    if "Limited methodology terminology" in critique_result["methodology"]:
        suggestions.append("Add detailed methodology section with research design")
    
    if "No explicit sample size found" in critique_result["methodology"]:
        suggestions.append("Include sample size and participant demographics")
    
    if "Limited statistical analysis terminology" in critique_result["methodology"]:
        suggestions.append("Report statistical tests and effect sizes")
    
    # Writing suggestions
    writing_flags = critique_result["writing_flags"]
    if any("Long average sentence length" in flag for flag in writing_flags):
        suggestions.append("Consider shorter, clearer sentences for better readability")
    
    if any("High passive voice" in flag for flag in writing_flags):
        suggestions.append("Reduce passive voice for more direct writing")
    
    if any("Academic jargon" in flag for flag in writing_flags):
        suggestions.append("Simplify technical language where possible")
    
    # Limitations suggestions
    limitations = critique_result["limitations"]
    if "No explicit limitations discussion found" in limitations:
        suggestions.append("Add dedicated limitations section")
    
    if "Limited discussion of generalizability" in limitations:
        suggestions.append("Discuss generalizability and external validity")
    
    if "No mention of data or code availability" in limitations:
        suggestions.append("Consider making data and analysis code available")
    
    # General suggestions
    novelty_terms = ['novel', 'new', 'innovative', 'first', 'original']
    novelty_count = sum(text.count(term) for term in novelty_terms)
    
    if novelty_count < 3:
        suggestions.append("Clarify the novel contributions of this work")
    
    # Check for future work
    if 'future work' not in text and 'future research' not in text:
        suggestions.append("Include discussion of future research directions")
    
    return suggestions[:8]  # Limit to 8 suggestions