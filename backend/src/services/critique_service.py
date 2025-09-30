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
        """Complete academic analysis: writing quality, statistical analysis, citations, literature, and advanced critique"""
        try:
            critique_result = {}
            
            # Priority 1 & 2: Core analysis
            methodology_analysis = self._analyze_methodology_advanced(text)
            critique_result.update(methodology_analysis)
            
            argument_analysis = self._evaluate_arguments_advanced(text)
            critique_result.update(argument_analysis)
            
            bias_analysis = self._detect_bias_comprehensive(text)
            critique_result.update(bias_analysis)
            
            validity_analysis = self._assess_validity_comprehensive(text)
            critique_result.update(validity_analysis)
            
            # 1. Academic Writing Quality
            writing_quality = self._analyze_academic_writing_quality(text)
            critique_result.update(writing_quality)
            
            # 2. Statistical Analysis
            statistical_analysis = self._analyze_statistical_quality(text)
            critique_result.update(statistical_analysis)
            
            # 3. Citation Network Analysis
            citation_analysis = self._analyze_citation_network(text)
            critique_result.update(citation_analysis)
            
            # 4. Literature Analysis
            literature_analysis = self._analyze_literature_quality(text)
            critique_result.update(literature_analysis)
            
            # 5. Advanced Critique Features
            advanced_critique = self._analyze_advanced_features(text)
            critique_result.update(advanced_critique)
            
            # Comprehensive assessment
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
    
    # 1. Academic Writing Quality Analysis
    def _analyze_academic_writing_quality(self, text):
        """Structure/coherence analysis, argument flow, abstract quality"""
        text_lower = text.lower()
        
        # Structure analysis
        structure_score = self._analyze_structure_coherence(text)
        
        # Argument flow evaluation
        argument_flow = self._evaluate_argument_flow(text)
        
        # Abstract quality assessment
        abstract_quality = self._assess_abstract_quality(text)
        
        writing_score = (structure_score["score"] + argument_flow["score"] + abstract_quality["score"]) / 3
        
        return {
            "writing_quality_analysis": {
                "structure_coherence": structure_score,
                "argument_flow": argument_flow,
                "abstract_quality": abstract_quality,
                "overall_writing_score": round(writing_score, 1)
            }
        }
    
    def _analyze_structure_coherence(self, text):
        """Analyze document structure and coherence"""
        sections = text.split('\n\n')  # Basic section detection
        
        # Check for logical section order
        section_keywords = {
            "title": ["title", "research", "study", "analysis"],
            "abstract": ["abstract", "summary"],
            "introduction": ["introduction", "background"],
            "methods": ["method", "methodology", "approach"],
            "results": ["results", "findings", "outcomes"],
            "discussion": ["discussion", "analysis", "interpretation"],
            "conclusion": ["conclusion", "summary", "implications"]
        }
        
        found_sections = []
        for section in sections:
            section_lower = section.lower()
            for section_type, keywords in section_keywords.items():
                if any(kw in section_lower for kw in keywords) and len(section) > 50:
                    found_sections.append(section_type)
                    break
        
        # Coherence indicators
        coherence_words = ["therefore", "however", "furthermore", "moreover", "consequently", "thus"]
        coherence_count = sum(text.lower().count(word) for word in coherence_words)
        
        structure_score = min(100, len(found_sections) * 12 + coherence_count * 3)
        
        return {
            "sections_found": found_sections,
            "coherence_indicators": coherence_count,
            "score": structure_score,
            "assessment": "Good" if structure_score > 70 else "Moderate" if structure_score > 50 else "Poor"
        }
    
    def _evaluate_argument_flow(self, text):
        """Evaluate logical flow and argument progression"""
        text_lower = text.lower()
        
        # Logical connectors
        flow_indicators = {
            "causal": ["because", "since", "due to", "as a result", "therefore"],
            "contrast": ["however", "but", "although", "despite", "nevertheless"],
            "addition": ["furthermore", "moreover", "additionally", "also", "in addition"],
            "sequence": ["first", "second", "then", "next", "finally", "subsequently"]
        }
        
        flow_analysis = {}
        total_indicators = 0
        
        for category, indicators in flow_indicators.items():
            count = sum(text_lower.count(indicator) for indicator in indicators)
            flow_analysis[category] = count
            total_indicators += count
        
        # Argument strength progression
        paragraphs = text.split('\n\n')
        evidence_density = []
        
        for para in paragraphs:
            if len(para) > 100:  # Substantial paragraphs only
                evidence_words = ["data", "evidence", "study", "research", "analysis", "results"]
                evidence_count = sum(para.lower().count(word) for word in evidence_words)
                evidence_density.append(evidence_count / max(len(para.split()), 1))
        
        avg_evidence_density = statistics.mean(evidence_density) if evidence_density else 0
        flow_score = min(100, total_indicators * 5 + avg_evidence_density * 1000)
        
        return {
            "logical_connectors": flow_analysis,
            "total_flow_indicators": total_indicators,
            "evidence_density": round(avg_evidence_density, 4),
            "score": round(flow_score, 1),
            "assessment": "Strong" if flow_score > 70 else "Moderate" if flow_score > 40 else "Weak"
        }
    
    def _assess_abstract_quality(self, text):
        """Assess abstract completeness and quality"""
        # Find abstract section
        text_lower = text.lower()
        abstract_start = text_lower.find("abstract")
        
        if abstract_start == -1:
            return {"score": 0, "assessment": "No abstract found", "components": {}}
        
        # Extract abstract (next 500 chars after "abstract")
        abstract_end = min(abstract_start + 800, len(text))
        abstract_text = text[abstract_start:abstract_end].lower()
        
        # Check for abstract components
        components = {
            "background": any(word in abstract_text for word in ["background", "context", "problem"]),
            "objective": any(word in abstract_text for word in ["objective", "aim", "purpose", "goal"]),
            "methods": any(word in abstract_text for word in ["method", "approach", "design", "study"]),
            "results": any(word in abstract_text for word in ["results", "findings", "outcomes"]),
            "conclusion": any(word in abstract_text for word in ["conclusion", "implications", "significance"])
        }
        
        component_score = sum(components.values()) * 20
        word_count = len(abstract_text.split())
        length_score = 100 if 150 <= word_count <= 300 else max(0, 100 - abs(word_count - 225) * 2)
        
        abstract_score = (component_score + length_score) / 2
        
        return {
            "components": components,
            "word_count": word_count,
            "component_score": component_score,
            "length_appropriateness": length_score,
            "score": round(abstract_score, 1),
            "assessment": "Excellent" if abstract_score > 85 else "Good" if abstract_score > 70 else "Adequate" if abstract_score > 50 else "Poor"
        }
    
    # 2. Statistical Analysis
    def _analyze_statistical_quality(self, text):
        """Significance testing, sample size adequacy, statistical assumptions"""
        text_lower = text.lower()
        
        # Significance testing evaluation
        significance_analysis = self._evaluate_significance_testing(text_lower)
        
        # Sample size adequacy
        sample_size_analysis = self._assess_sample_size_adequacy(text_lower)
        
        # Statistical assumptions checking
        assumptions_analysis = self._check_statistical_assumptions(text_lower)
        
        statistical_score = (significance_analysis["score"] + sample_size_analysis["score"] + assumptions_analysis["score"]) / 3
        
        return {
            "statistical_analysis": {
                "significance_testing": significance_analysis,
                "sample_size_adequacy": sample_size_analysis,
                "statistical_assumptions": assumptions_analysis,
                "overall_statistical_score": round(statistical_score, 1)
            }
        }
    
    def _evaluate_significance_testing(self, text_lower):
        """Evaluate proper use of significance testing"""
        # Statistical test mentions
        statistical_tests = {
            "t_test": ["t-test", "t test", "student's t"],
            "anova": ["anova", "analysis of variance"],
            "chi_square": ["chi-square", "chi square", "χ²"],
            "regression": ["regression", "linear model"],
            "correlation": ["correlation", "pearson", "spearman"],
            "non_parametric": ["mann-whitney", "wilcoxon", "kruskal-wallis"]
        }
        
        tests_found = []
        for test_type, indicators in statistical_tests.items():
            if any(indicator in text_lower for indicator in indicators):
                tests_found.append(test_type)
        
        # P-value reporting
        p_value_patterns = [r'p\s*[<>=]\s*0\.\d+', r'p\s*[<>=]\s*\.\d+', r'p\s*[<>=]\s*\d+\.\d+']
        p_values_found = []
        for pattern in p_value_patterns:
            matches = re.findall(pattern, text_lower)
            p_values_found.extend(matches)
        
        # Effect size reporting
        effect_size_terms = ["effect size", "cohen's d", "eta squared", "r squared", "odds ratio"]
        effect_sizes_found = [term for term in effect_size_terms if term in text_lower]
        
        # Confidence intervals
        ci_indicators = ["confidence interval", "ci", "95% ci", "99% ci"]
        ci_found = any(indicator in text_lower for indicator in ci_indicators)
        
        significance_score = min(100, len(tests_found) * 25 + len(p_values_found) * 15 + len(effect_sizes_found) * 20 + (30 if ci_found else 0))
        
        return {
            "statistical_tests_found": tests_found,
            "p_values_reported": len(p_values_found),
            "effect_sizes_reported": effect_sizes_found,
            "confidence_intervals": ci_found,
            "score": significance_score,
            "assessment": "Comprehensive" if significance_score > 80 else "Adequate" if significance_score > 50 else "Insufficient"
        }
    
    def _assess_sample_size_adequacy(self, text_lower):
        """Assess sample size and power analysis"""
        # Extract sample sizes
        sample_patterns = [r'n\s*=\s*(\d+)', r'sample size.*?(\d+)', r'(\d+)\s+participants', r'(\d+)\s+subjects']
        sample_sizes = []
        
        for pattern in sample_patterns:
            matches = re.findall(pattern, text_lower)
            sample_sizes.extend([int(m) for m in matches if m.isdigit()])
        
        # Power analysis mentions
        power_indicators = ["power analysis", "power calculation", "statistical power", "beta"]
        power_analysis_found = any(indicator in text_lower for indicator in power_indicators)
        
        # Sample size justification
        justification_terms = ["sample size justification", "power", "effect size", "alpha level"]
        justification_found = sum(text_lower.count(term) for term in justification_terms)
        
        if sample_sizes:
            max_sample = max(sample_sizes)
            sample_adequacy = "Large" if max_sample > 100 else "Medium" if max_sample > 30 else "Small"
            adequacy_score = 100 if max_sample > 100 else 70 if max_sample > 30 else 30
        else:
            sample_adequacy = "Not reported"
            adequacy_score = 0
        
        power_score = 30 if power_analysis_found else 0
        justification_score = min(40, justification_found * 10)
        
        total_score = adequacy_score * 0.6 + power_score + justification_score
        
        return {
            "sample_sizes_found": sample_sizes,
            "largest_sample": max(sample_sizes) if sample_sizes else 0,
            "sample_adequacy": sample_adequacy,
            "power_analysis_mentioned": power_analysis_found,
            "justification_level": justification_found,
            "score": round(total_score, 1),
            "assessment": "Strong" if total_score > 80 else "Moderate" if total_score > 50 else "Weak"
        }
    
    def _check_statistical_assumptions(self, text_lower):
        """Check for statistical assumptions discussion"""
        assumptions = {
            "normality": ["normality", "normal distribution", "shapiro-wilk", "kolmogorov-smirnov"],
            "homogeneity": ["homogeneity", "equal variances", "levene", "bartlett"],
            "independence": ["independence", "independent observations", "autocorrelation"],
            "linearity": ["linearity", "linear relationship", "scatterplot"],
            "multicollinearity": ["multicollinearity", "vif", "tolerance"]
        }
        
        assumptions_checked = {}
        total_score = 0
        
        for assumption, indicators in assumptions.items():
            found = any(indicator in text_lower for indicator in indicators)
            assumptions_checked[assumption] = found
            if found:
                total_score += 20
        
        # General assumption discussion
        general_assumption_terms = ["assumptions", "violated", "met", "checked", "tested"]
        general_mentions = sum(text_lower.count(term) for term in general_assumption_terms)
        
        assumption_score = min(100, total_score + general_mentions * 5)
        
        return {
            "assumptions_checked": assumptions_checked,
            "assumptions_count": sum(assumptions_checked.values()),
            "general_assumption_discussion": general_mentions,
            "score": assumption_score,
            "assessment": "Thorough" if assumption_score > 70 else "Partial" if assumption_score > 30 else "Minimal"
        }
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

    # 3. Citation Network Analysis
    def _analyze_citation_network(self, text):
        """Citation patterns, impact factors, cross-reference validation"""
        # Extract citations from text
        citations = self._extract_citations_advanced(text)
        
        # Analyze citation patterns
        citation_patterns = self._analyze_citation_patterns(citations, text)
        
        # Assess impact factors (heuristic)
        impact_assessment = self._assess_citation_impact(citations)
        
        # Cross-reference validation
        cross_ref_validation = self._validate_cross_references(text)
        
        citation_score = (citation_patterns["score"] + impact_assessment["score"] + cross_ref_validation["score"]) / 3
        
        return {
            "citation_network_analysis": {
                "citation_patterns": citation_patterns,
                "impact_assessment": impact_assessment,
                "cross_reference_validation": cross_ref_validation,
                "overall_citation_score": round(citation_score, 1)
            }
        }
    
    def _extract_citations_advanced(self, text):
        """Extract citations with detailed pattern matching"""
        citations = []
        
        # APA style citations (Author, Year)
        apa_pattern = r'\(([A-Z][A-Za-z\-]+(?:\s*&\s*[A-Z][A-Za-z\-]+)*)\s*,\s*(\d{4}[a-z]?)\)'
        apa_matches = re.findall(apa_pattern, text)
        
        # Numbered citations [1], [2]
        numbered_pattern = r'\[(\d+)\]'
        numbered_matches = re.findall(numbered_pattern, text)
        
        # Reference list extraction
        ref_section = self._extract_reference_section(text)
        
        return {
            "apa_citations": apa_matches,
            "numbered_citations": numbered_matches,
            "reference_list": ref_section,
            "total_citations": len(apa_matches) + len(numbered_matches) + len(ref_section)
        }
    
    def _analyze_citation_patterns(self, citations, text):
        """Analyze citation distribution and patterns"""
        total_citations = citations["total_citations"]
        word_count = len(text.split())
        
        # Citation density (citations per 1000 words)
        citation_density = (total_citations / max(word_count, 1)) * 1000
        
        # Citation age analysis (extract years)
        years = []
        for author, year in citations["apa_citations"]:
            try:
                year_num = int(year[:4])
                years.append(year_num)
            except:
                continue
        
        # Currency assessment (how recent are citations)
        current_year = 2024
        recent_citations = len([year for year in years if current_year - year <= 5])
        currency_ratio = recent_citations / max(len(years), 1)
        
        # Citation distribution score
        distribution_score = min(100, citation_density * 20)
        currency_score = currency_ratio * 100
        
        pattern_score = (distribution_score + currency_score) / 2
        
        return {
            "citation_density": round(citation_density, 2),
            "total_citations": total_citations,
            "recent_citations_ratio": round(currency_ratio, 2),
            "average_citation_age": round(statistics.mean([current_year - year for year in years]), 1) if years else 0,
            "score": round(pattern_score, 1),
            "assessment": "Excellent" if pattern_score > 80 else "Good" if pattern_score > 60 else "Adequate" if pattern_score > 40 else "Poor"
        }
    
    def _assess_citation_impact(self, citations):
        """Heuristic assessment of citation impact"""
        ref_list = citations["reference_list"]
        
        # High-impact journal indicators
        high_impact_journals = [
            "nature", "science", "cell", "lancet", "nejm", "jama",
            "pnas", "journal of", "proceedings of", "review of"
        ]
        
        high_impact_count = 0
        for ref in ref_list:
            ref_lower = ref.lower()
            if any(journal in ref_lower for journal in high_impact_journals):
                high_impact_count += 1
        
        # Self-citation detection (heuristic)
        first_author_names = set()
        self_citations = 0
        
        for ref in ref_list[:5]:  # Check first 5 references for author patterns
            # Extract potential author names (first word before comma)
            author_match = re.match(r'^([A-Z][a-z]+)', ref)
            if author_match:
                first_author_names.add(author_match.group(1))
        
        # Diversity assessment
        diversity_score = min(100, len(set(ref_list)) * 5)  # Penalize duplicate refs
        impact_score = (high_impact_count / max(len(ref_list), 1)) * 100
        
        overall_impact = (diversity_score + impact_score) / 2
        
        return {
            "high_impact_citations": high_impact_count,
            "citation_diversity": len(set(ref_list)),
            "potential_self_citations": self_citations,
            "impact_ratio": round(impact_score / 100, 2),
            "score": round(overall_impact, 1),
            "assessment": "High" if overall_impact > 70 else "Medium" if overall_impact > 40 else "Low"
        }
    
    def _validate_cross_references(self, text):
        """Validate internal cross-references"""
        text_lower = text.lower()
        
        # Table/Figure references
        table_refs = len(re.findall(r'\btable\s+\d+', text_lower))
        figure_refs = len(re.findall(r'\bfigure\s+\d+', text_lower))
        section_refs = len(re.findall(r'\bsection\s+\d+', text_lower))
        
        # Equation references
        equation_refs = len(re.findall(r'\bequation\s+\d+', text_lower))
        
        # Appendix references
        appendix_refs = len(re.findall(r'\bappendix\s+[a-z]', text_lower))
        
        total_internal_refs = table_refs + figure_refs + section_refs + equation_refs + appendix_refs
        
        # Cross-reference quality score
        cross_ref_score = min(100, total_internal_refs * 10)
        
        return {
            "table_references": table_refs,
            "figure_references": figure_refs,
            "section_references": section_refs,
            "equation_references": equation_refs,
            "appendix_references": appendix_refs,
            "total_internal_references": total_internal_refs,
            "score": cross_ref_score,
            "assessment": "Comprehensive" if cross_ref_score > 70 else "Adequate" if cross_ref_score > 30 else "Minimal"
        }
    
    # 4. Literature Analysis
    def _analyze_literature_quality(self, text):
        """Gap detection, novelty assessment, research positioning"""
        text_lower = text.lower()
        
        # Gap detection
        gap_analysis = self._detect_research_gaps(text_lower)
        
        # Novelty assessment
        novelty_analysis = self._assess_research_novelty(text_lower)
        
        # Research positioning
        positioning_analysis = self._analyze_research_positioning(text_lower)
        
        literature_score = (gap_analysis["score"] + novelty_analysis["score"] + positioning_analysis["score"]) / 3
        
        return {
            "literature_analysis": {
                "research_gaps": gap_analysis,
                "novelty_assessment": novelty_analysis,
                "research_positioning": positioning_analysis,
                "overall_literature_score": round(literature_score, 1)
            }
        }
    
    def _detect_research_gaps(self, text_lower):
        """Detect discussion of research gaps"""
        gap_indicators = [
            "gap", "limitation", "shortcoming", "lack of", "absence of",
            "missing", "insufficient", "limited research", "few studies",
            "no previous", "understudied", "under-researched", "overlooked"
        ]
        
        gap_mentions = sum(text_lower.count(indicator) for indicator in gap_indicators)
        
        # Gap specificity - look for specific gap descriptions
        specific_gaps = [
            "methodological gap", "theoretical gap", "empirical gap",
            "knowledge gap", "research gap", "literature gap"
        ]
        
        specific_gap_count = sum(text_lower.count(gap) for gap in specific_gaps)
        
        gap_score = min(100, gap_mentions * 15 + specific_gap_count * 25)
        
        return {
            "gap_indicators_found": gap_mentions,
            "specific_gaps_mentioned": specific_gap_count,
            "score": gap_score,
            "assessment": "Well-identified" if gap_score > 70 else "Partially identified" if gap_score > 30 else "Poorly identified"
        }
    
    def _assess_research_novelty(self, text_lower):
        """Assess claims of novelty and originality"""
        novelty_terms = [
            "novel", "new", "innovative", "original", "first", "unique",
            "unprecedented", "groundbreaking", "pioneering", "cutting-edge"
        ]
        
        novelty_claims = sum(text_lower.count(term) for term in novelty_terms)
        
        # Contribution clarity
        contribution_terms = [
            "contribution", "contributions", "advance", "advancement",
            "breakthrough", "discovery", "finding", "insight"
        ]
        
        contribution_mentions = sum(text_lower.count(term) for term in contribution_terms)
        
        # Innovation indicators
        innovation_terms = [
            "method", "approach", "technique", "framework", "model",
            "algorithm", "system", "tool", "protocol"
        ]
        
        innovation_count = sum(text_lower.count(term) for term in innovation_terms)
        
        novelty_score = min(100, novelty_claims * 10 + contribution_mentions * 15 + innovation_count * 5)
        
        return {
            "novelty_claims": novelty_claims,
            "contribution_mentions": contribution_mentions,
            "innovation_indicators": innovation_count,
            "score": novelty_score,
            "assessment": "Strong novelty" if novelty_score > 80 else "Moderate novelty" if novelty_score > 50 else "Limited novelty"
        }
    
    def _analyze_research_positioning(self, text_lower):
        """Analyze how research is positioned in the field"""
        # Field positioning
        field_terms = [
            "field", "domain", "area", "discipline", "research area",
            "literature", "previous work", "existing research", "current state"
        ]
        
        positioning_mentions = sum(text_lower.count(term) for term in field_terms)
        
        # Comparison with existing work
        comparison_terms = [
            "compared to", "in contrast to", "unlike", "different from",
            "similar to", "builds on", "extends", "improves upon"
        ]
        
        comparison_count = sum(text_lower.count(term) for term in comparison_terms)
        
        # Future directions
        future_terms = [
            "future work", "future research", "next steps", "further study",
            "future directions", "ongoing work", "planned research"
        ]
        
        future_mentions = sum(text_lower.count(term) for term in future_terms)
        
        positioning_score = min(100, positioning_mentions * 8 + comparison_count * 15 + future_mentions * 20)
        
        return {
            "field_positioning": positioning_mentions,
            "comparison_with_existing": comparison_count,
            "future_directions": future_mentions,
            "score": positioning_score,
            "assessment": "Well-positioned" if positioning_score > 70 else "Moderately positioned" if positioning_score > 40 else "Poorly positioned"
        }
    
    # 5. Advanced Critique Features
    def _analyze_advanced_features(self, text):
        """Reproducibility assessment, peer review metrics, reference format validation"""
        text_lower = text.lower()
        
        # Reproducibility assessment
        reproducibility = self._assess_reproducibility(text_lower)
        
        # Peer review metrics (heuristic indicators)
        peer_review = self._analyze_peer_review_metrics(text_lower)
        
        # Reference format validation
        reference_format = self._validate_reference_format(text)
        
        advanced_score = (reproducibility["score"] + peer_review["score"] + reference_format["score"]) / 3
        
        return {
            "advanced_critique_features": {
                "reproducibility_assessment": reproducibility,
                "peer_review_metrics": peer_review,
                "reference_format_validation": reference_format,
                "overall_advanced_score": round(advanced_score, 1)
            }
        }
    
    def _assess_reproducibility(self, text_lower):
        """Assess research reproducibility"""
        reproducibility_indicators = [
            "reproducible", "replicable", "data available", "code available",
            "open source", "github", "repository", "supplementary materials",
            "appendix", "detailed methods", "step-by-step", "protocol"
        ]
        
        reproducibility_count = sum(text_lower.count(indicator) for indicator in reproducibility_indicators)
        
        # Data sharing indicators
        data_sharing = [
            "data sharing", "open data", "dataset", "raw data",
            "supplementary data", "data repository", "figshare", "zenodo"
        ]
        
        data_sharing_count = sum(text_lower.count(term) for term in data_sharing)
        
        # Method detail assessment
        method_detail_terms = [
            "procedure", "protocol", "step", "parameter", "setting",
            "configuration", "implementation", "algorithm", "formula"
        ]
        
        method_detail_count = sum(text_lower.count(term) for term in method_detail_terms)
        
        reproducibility_score = min(100, reproducibility_count * 15 + data_sharing_count * 20 + method_detail_count * 5)
        
        return {
            "reproducibility_indicators": reproducibility_count,
            "data_sharing_mentions": data_sharing_count,
            "method_detail_level": method_detail_count,
            "score": reproducibility_score,
            "assessment": "Highly reproducible" if reproducibility_score > 80 else "Moderately reproducible" if reproducibility_score > 50 else "Low reproducibility"
        }
    
    def _analyze_peer_review_metrics(self, text_lower):
        """Analyze indicators of peer review quality"""
        peer_review_indicators = [
            "peer review", "reviewed", "referee", "reviewer comments",
            "blind review", "double-blind", "editorial", "revision"
        ]
        
        peer_review_mentions = sum(text_lower.count(indicator) for indicator in peer_review_indicators)
        
        # Quality indicators
        quality_indicators = [
            "rigorous", "thorough", "comprehensive", "detailed review",
            "expert review", "independent review", "external review"
        ]
        
        quality_count = sum(text_lower.count(indicator) for indicator in quality_indicators)
        
        # Journal quality hints
        journal_quality_terms = [
            "impact factor", "indexed", "scopus", "web of science",
            "prestigious", "leading journal", "top-tier"
        ]
        
        journal_quality_count = sum(text_lower.count(term) for term in journal_quality_terms)
        
        peer_review_score = min(100, peer_review_mentions * 20 + quality_count * 15 + journal_quality_count * 25)
        
        return {
            "peer_review_mentions": peer_review_mentions,
            "quality_indicators": quality_count,
            "journal_quality_hints": journal_quality_count,
            "score": peer_review_score,
            "assessment": "High quality review" if peer_review_score > 70 else "Standard review" if peer_review_score > 30 else "Limited review indicators"
        }
    
    def _validate_reference_format(self, text):
        """Validate reference formatting consistency"""
        # Extract reference section
        ref_section = self._extract_reference_section(text)
        
        if not ref_section:
            return {"score": 0, "assessment": "No reference section found", "format_consistency": 0}
        
        # Check formatting patterns
        apa_pattern = r'^[A-Z][a-z]+.*\(\d{4}\)'  # Author (Year) pattern
        numbered_pattern = r'^\[\d+\]'  # [1] pattern
        
        apa_count = sum(1 for ref in ref_section if re.match(apa_pattern, ref))
        numbered_count = sum(1 for ref in ref_section if re.match(numbered_pattern, ref))
        
        # Format consistency
        total_refs = len(ref_section)
        max_format_count = max(apa_count, numbered_count)
        consistency_ratio = max_format_count / max(total_refs, 1)
        
        # DOI presence
        doi_count = sum(1 for ref in ref_section if 'doi' in ref.lower() or '10.' in ref)
        doi_ratio = doi_count / max(total_refs, 1)
        
        format_score = consistency_ratio * 70 + doi_ratio * 30
        
        return {
            "total_references": total_refs,
            "apa_format_count": apa_count,
            "numbered_format_count": numbered_count,
            "format_consistency_ratio": round(consistency_ratio, 2),
            "doi_presence_ratio": round(doi_ratio, 2),
            "score": round(format_score, 1),
            "assessment": "Excellent formatting" if format_score > 85 else "Good formatting" if format_score > 70 else "Inconsistent formatting"
        }
    
    def _extract_reference_section(self, text):
        """Extract references from the paper"""
        text_lower = text.lower()
        
        # Find references section
        ref_patterns = ["references", "bibliography", "works cited"]
        ref_start = -1
        
        for pattern in ref_patterns:
            pos = text_lower.find(pattern)
            if pos != -1:
                ref_start = pos
                break
        
        if ref_start == -1:
            return []
        
        # Extract references section
        ref_text = text[ref_start:]
        ref_lines = ref_text.split('\n')
        
        references = []
        for line in ref_lines[1:]:  # Skip header
            line = line.strip()
            if len(line) > 30 and not line.lower().startswith(('references', 'bibliography')):
                references.append(line)
                if len(references) >= 50:  # Limit extraction
                    break
        
        return references

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