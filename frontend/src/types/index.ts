export interface Citation {
  reference: string;
  valid: boolean;
}

export interface FactCheckResult {
  claim: string;
  status: string;
}

export interface AnalysisStats {
  word_count: number;
  plagiarism_percent?: number;
  citations_count?: number;
  analysis_date?: string;
}

// Enhanced comprehensive analysis interfaces
export interface WritingQualityAnalysis {
  structure_coherence: {
    sections_found: string[];
    coherence_indicators: number;
    score: number;
    assessment: string;
  };
  argument_flow: {
    logical_connectors: Record<string, number>;
    total_flow_indicators: number;
    evidence_density: number;
    score: number;
    assessment: string;
  };
  abstract_quality: {
    components: Record<string, boolean>;
    word_count: number;
    component_score: number;
    length_appropriateness: number;
    score: number;
    assessment: string;
  };
  overall_writing_score: number;
}

export interface StatisticalAnalysis {
  significance_testing: {
    statistical_tests_found: string[];
    p_values_reported: number;
    effect_sizes_reported: string[];
    confidence_intervals: boolean;
    score: number;
    assessment: string;
  };
  sample_size_adequacy: {
    sample_sizes_found: number[];
    largest_sample: number;
    sample_adequacy: string;
    power_analysis_mentioned: boolean;
    justification_level: number;
    score: number;
    assessment: string;
  };
  statistical_assumptions: {
    assumptions_checked: Record<string, boolean>;
    assumptions_count: number;
    general_assumption_discussion: number;
    score: number;
    assessment: string;
  };
  overall_statistical_score: number;
}

export interface CitationNetworkAnalysis {
  citation_patterns: {
    citation_density: number;
    total_citations: number;
    recent_citations_ratio: number;
    average_citation_age: number;
    score: number;
    assessment: string;
  };
  impact_assessment: {
    high_impact_citations: number;
    citation_diversity: number;
    potential_self_citations: number;
    impact_ratio: number;
    score: number;
    assessment: string;
  };
  cross_reference_validation: {
    table_references: number;
    figure_references: number;
    section_references: number;
    equation_references: number;
    appendix_references: number;
    total_internal_references: number;
    score: number;
    assessment: string;
  };
  overall_citation_score: number;
}

export interface LiteratureAnalysis {
  research_gaps: {
    gap_indicators_found: number;
    specific_gaps_mentioned: number;
    score: number;
    assessment: string;
  };
  novelty_assessment: {
    novelty_claims: number;
    contribution_mentions: number;
    innovation_indicators: number;
    score: number;
    assessment: string;
  };
  research_positioning: {
    field_positioning: number;
    comparison_with_existing: number;
    future_directions: number;
    score: number;
    assessment: string;
  };
  overall_literature_score: number;
}

export interface AdvancedCritiqueFeatures {
  reproducibility_assessment: {
    reproducibility_indicators: number;
    data_sharing_mentions: number;
    method_detail_level: number;
    score: number;
    assessment: string;
  };
  peer_review_metrics: {
    peer_review_mentions: number;
    quality_indicators: number;
    journal_quality_hints: number;
    score: number;
    assessment: string;
  };
  reference_format_validation: {
    total_references: number;
    apa_format_count: number;
    numbered_format_count: number;
    format_consistency_ratio: number;
    doi_presence_ratio: number;
    score: number;
    assessment: string;
  };
  overall_advanced_score: number;
}

export interface ComprehensiveCritique {
  // Priority 1 & 2 Core Analysis
  methodology_frameworks_detected: string[];
  framework_analysis: Record<string, any>;
  sample_size_analysis: {
    sizes_found: number[];
    adequate: boolean;
  };
  statistical_rigor: {
    terms_found: string[];
    count: number;
  };
  methodology_quality_score: number;

  claim_strength_analysis: Record<string, any>;
  evidence_support_ratio: number;
  logical_flow_indicators: number;
  argument_quality_score: number;

  bias_types_analysis: Record<string, any>;
  language_objectivity: {
    ratio: number;
    assessment: string;
  };
  statistical_bias_indicators: string[];
  overall_bias_risk: string;
  bias_score: number;

  validity_analysis: Record<string, any>;
  overall_validity_score: number;
  validity_grade: string;

  // 5 Feature Categories
  writing_quality_analysis: WritingQualityAnalysis;
  statistical_analysis: StatisticalAnalysis;
  citation_network_analysis: CitationNetworkAnalysis;
  literature_analysis: LiteratureAnalysis;
  advanced_critique_features: AdvancedCritiqueFeatures;

  // Overall Assessment
  overall_assessment: {
    overall_score: number;
    grade: string;
    category: string;
  };
  academic_recommendations: string[];
  quality_grade: {
    grade: string;
    description: string;
  };
}

export interface AnalysisResponse {
  summary: string;
  plagiarism: any; // Keep flexible for backward compatibility
  citations: any; // Keep flexible for backward compatibility
  critique: ComprehensiveCritique;
  quality_metrics?: any;
  overall_quality_score?: number;
  stats: AnalysisStats;
  // Legacy fields for backward compatibility
  fact_check?: {
    facts: FactCheckResult[];
  };
}

export interface ApiError {
  error: string;
}