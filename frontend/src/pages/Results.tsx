import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AnalysisResponse } from '../types';

interface ScoreCardProps {
  title: string;
  score: number;
  assessment: string;
  icon: string;
  details?: React.ReactNode;
}

const ScoreCard: React.FC<ScoreCardProps> = ({ title, score, assessment, icon, details }) => {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-100';
    if (score >= 60) return 'text-yellow-600 bg-yellow-100';
    if (score >= 40) return 'text-orange-600 bg-orange-100';
    return 'text-red-600 bg-red-100';
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <div className={`text-2xl ${icon}`}></div>
      </div>
      <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(score)} mb-2`}>
        {score.toFixed(1)}/100
      </div>
      <p className="text-sm text-gray-600 mb-2">{assessment}</p>
      {details && <div className="mt-3 text-xs text-gray-500">{details}</div>}
    </div>
  );
};

interface ExpandableCardProps {
  title: string;
  children: React.ReactNode;
  defaultExpanded?: boolean;
}

const ExpandableCard: React.FC<ExpandableCardProps> = ({ title, children, defaultExpanded = false }) => {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  return (
    <div className="bg-white rounded-lg shadow">
      <div 
        className="p-6 cursor-pointer border-b border-gray-200 hover:bg-gray-50"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
          <svg 
            className={`w-5 h-5 transform transition-transform ${isExpanded ? 'rotate-180' : ''}`}
            fill="currentColor" 
            viewBox="0 0 20 20"
          >
            <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </div>
      </div>
      {isExpanded && (
        <div className="p-6">
          {children}
        </div>
      )}
    </div>
  );
};

const Results: React.FC = () => {
  const [results, setResults] = useState<AnalysisResponse | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedResults = sessionStorage.getItem('analysisResults');
    if (storedResults) {
      try {
        setResults(JSON.parse(storedResults));
      } catch (error) {
        console.error('Failed to parse stored results:', error);
        navigate('/');
      }
    } else {
      navigate('/');
    }
  }, [navigate]);

  if (!results) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading results...</p>
        </div>
      </div>
    );
  }

  const getPlagiarismColor = (score: number) => {
    if (score < 15) return 'text-green-600 bg-green-100';
    if (score < 30) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getPlagiarismLabel = (score: number) => {
    if (score < 15) return 'Low Risk';
    if (score < 30) return 'Medium Risk';
    return 'High Risk';
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-100';
    if (score >= 60) return 'text-yellow-600 bg-yellow-100';
    if (score >= 40) return 'text-orange-600 bg-orange-100';
    return 'text-red-600 bg-red-100';
  };

  // Handle both new comprehensive format and legacy format
  const critique = results.critique;
  const hasCritique = critique && typeof critique === 'object';
  const plagiarismScore = typeof results.plagiarism === 'number' ? results.plagiarism : (results.plagiarism?.plagiarism_score || 0);

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Comprehensive Academic Analysis Results
          </h1>
          <button
            onClick={() => navigate('/')}
            className="text-blue-600 hover:text-blue-700 font-medium"
          >
            ← Analyze Another Document
          </button>
        </div>

        {/* Overall Quality Score */}
        {hasCritique && critique.overall_assessment && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Overall Academic Quality</h2>
              <div className={`inline-flex items-center px-6 py-3 rounded-full text-2xl font-bold ${getScoreColor(critique.overall_assessment.overall_score)} mb-4`}>
                {critique.overall_assessment.overall_score.toFixed(1)}/100 - Grade {critique.overall_assessment.grade}
              </div>
              <p className="text-lg text-gray-600 mb-4">{critique.overall_assessment.category}</p>
              {critique.quality_grade && (
                <p className="text-sm text-gray-500">{critique.quality_grade.description}</p>
              )}
            </div>
          </div>
        )}

        {/* Quick Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <svg className="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
                    <path fillRule="evenodd" d="M4 5a2 2 0 012-2v1a1 1 0 102 0V3a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 2a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd"/>
                  </svg>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Word Count
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {results.stats.word_count.toLocaleString()}
                  </dd>
                </dl>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${getPlagiarismColor(plagiarismScore)}`}>
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd"/>
                  </svg>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Plagiarism Risk
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {plagiarismScore.toFixed(1)}% - {getPlagiarismLabel(plagiarismScore)}
                  </dd>
                </dl>
              </div>
            </div>
          </div>

          {hasCritique && critique.methodology_quality_score !== undefined && (
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${getScoreColor(critique.methodology_quality_score)}`}>
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Methodology
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {critique.methodology_quality_score.toFixed(1)}/100
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          )}

          {hasCritique && critique.overall_validity_score !== undefined && (
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${getScoreColor(critique.overall_validity_score)}`}>
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M3 6a3 3 0 013-3h10a1 1 0 01.8 1.6L14.25 8l2.55 3.4A1 1 0 0116 13H6a1 1 0 00-1 1v3a1 1 0 11-2 0V6z" clipRule="evenodd"/>
                    </svg>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Validity Grade
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {critique.validity_grade} ({critique.overall_validity_score.toFixed(1)})
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Main Analysis Sections */}
        <div className="space-y-6">
          {/* AI Summary */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                📄 AI Summary
              </h2>
              <div className="prose prose-sm max-w-none">
                <p className="text-gray-700 leading-relaxed">
                  {results.summary}
                </p>
              </div>
            </div>
          </div>

          {/* Comprehensive Academic Analysis */}
          {hasCritique && (
            <div className="space-y-6">
              {/* 1. Academic Writing Quality */}
              {critique.writing_quality_analysis && (
                <div className="bg-white rounded-lg shadow">
                  <div className="p-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-6">
                      ✍️ Academic Writing Quality
                      <span className={`ml-4 inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(critique.writing_quality_analysis.overall_writing_score)}`}>
                        {critique.writing_quality_analysis.overall_writing_score.toFixed(1)}/100
                      </span>
                    </h2>
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      {/* Structure & Coherence */}
                      <div className="border border-gray-200 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 mb-2">Structure & Coherence</h3>
                        <div className={`inline-flex items-center px-2 py-1 rounded text-sm font-medium ${getScoreColor(critique.writing_quality_analysis.structure_coherence.score)} mb-2`}>
                          {critique.writing_quality_analysis.structure_coherence.score}/100
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{critique.writing_quality_analysis.structure_coherence.assessment}</p>
                        <div className="text-xs text-gray-500">
                          <p>Sections found: {critique.writing_quality_analysis.structure_coherence.sections_found.length}</p>
                          <p>Coherence indicators: {critique.writing_quality_analysis.structure_coherence.coherence_indicators}</p>
                        </div>
                      </div>

                      {/* Argument Flow */}
                      <div className="border border-gray-200 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 mb-2">Argument Flow</h3>
                        <div className={`inline-flex items-center px-2 py-1 rounded text-sm font-medium ${getScoreColor(critique.writing_quality_analysis.argument_flow.score)} mb-2`}>
                          {critique.writing_quality_analysis.argument_flow.score.toFixed(1)}/100
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{critique.writing_quality_analysis.argument_flow.assessment}</p>
                        <div className="text-xs text-gray-500">
                          <p>Flow indicators: {critique.writing_quality_analysis.argument_flow.total_flow_indicators}</p>
                          <p>Evidence density: {critique.writing_quality_analysis.argument_flow.evidence_density}</p>
                        </div>
                      </div>

                      {/* Abstract Quality */}
                      <div className="border border-gray-200 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 mb-2">Abstract Quality</h3>
                        <div className={`inline-flex items-center px-2 py-1 rounded text-sm font-medium ${getScoreColor(critique.writing_quality_analysis.abstract_quality.score)} mb-2`}>
                          {critique.writing_quality_analysis.abstract_quality.score.toFixed(1)}/100
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{critique.writing_quality_analysis.abstract_quality.assessment}</p>
                        <div className="text-xs text-gray-500">
                          <p>Word count: {critique.writing_quality_analysis.abstract_quality.word_count}</p>
                          <p>Components: {Object.values(critique.writing_quality_analysis.abstract_quality.components).filter(Boolean).length}/5</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* 2. Statistical Analysis */}
              {critique.statistical_analysis && (
                <div className="bg-white rounded-lg shadow">
                  <div className="p-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-6">
                      📊 Statistical Analysis
                      <span className={`ml-4 inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(critique.statistical_analysis.overall_statistical_score)}`}>
                        {critique.statistical_analysis.overall_statistical_score.toFixed(1)}/100
                      </span>
                    </h2>
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      {/* Significance Testing */}
                      <div className="border border-gray-200 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 mb-2">Significance Testing</h3>
                        <div className={`inline-flex items-center px-2 py-1 rounded text-sm font-medium ${getScoreColor(critique.statistical_analysis.significance_testing.score)} mb-2`}>
                          {critique.statistical_analysis.significance_testing.score}/100
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{critique.statistical_analysis.significance_testing.assessment}</p>
                        <div className="text-xs text-gray-500">
                          <p>Tests found: {critique.statistical_analysis.significance_testing.statistical_tests_found.length}</p>
                          <p>P-values reported: {critique.statistical_analysis.significance_testing.p_values_reported}</p>
                          <p>Effect sizes: {critique.statistical_analysis.significance_testing.effect_sizes_reported.length}</p>
                        </div>
                      </div>

                      {/* Sample Size */}
                      <div className="border border-gray-200 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 mb-2">Sample Size Adequacy</h3>
                        <div className={`inline-flex items-center px-2 py-1 rounded text-sm font-medium ${getScoreColor(critique.statistical_analysis.sample_size_adequacy.score)} mb-2`}>
                          {critique.statistical_analysis.sample_size_adequacy.score.toFixed(1)}/100
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{critique.statistical_analysis.sample_size_adequacy.assessment}</p>
                        <div className="text-xs text-gray-500">
                          <p>Largest sample: {critique.statistical_analysis.sample_size_adequacy.largest_sample}</p>
                          <p>Adequacy: {critique.statistical_analysis.sample_size_adequacy.sample_adequacy}</p>
                          <p>Power analysis: {critique.statistical_analysis.sample_size_adequacy.power_analysis_mentioned ? 'Yes' : 'No'}</p>
                        </div>
                      </div>

                      {/* Statistical Assumptions */}
                      <div className="border border-gray-200 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 mb-2">Statistical Assumptions</h3>
                        <div className={`inline-flex items-center px-2 py-1 rounded text-sm font-medium ${getScoreColor(critique.statistical_analysis.statistical_assumptions.score)} mb-2`}>
                          {critique.statistical_analysis.statistical_assumptions.score}/100
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{critique.statistical_analysis.statistical_assumptions.assessment}</p>
                        <div className="text-xs text-gray-500">
                          <p>Assumptions checked: {critique.statistical_analysis.statistical_assumptions.assumptions_count}/5</p>
                          <p>General discussion: {critique.statistical_analysis.statistical_assumptions.general_assumption_discussion}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* 3. Citation Network Analysis */}
              {critique.citation_network_analysis && (
                <div className="bg-white rounded-lg shadow">
                  <div className="p-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-6">
                      📚 Citation Network Analysis
                      <span className={`ml-4 inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(critique.citation_network_analysis.overall_citation_score)}`}>
                        {critique.citation_network_analysis.overall_citation_score.toFixed(1)}/100
                      </span>
                    </h2>
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      {/* Citation Patterns */}
                      <div className="border border-gray-200 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 mb-2">Citation Patterns</h3>
                        <div className={`inline-flex items-center px-2 py-1 rounded text-sm font-medium ${getScoreColor(critique.citation_network_analysis.citation_patterns.score)} mb-2`}>
                          {critique.citation_network_analysis.citation_patterns.score.toFixed(1)}/100
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{critique.citation_network_analysis.citation_patterns.assessment}</p>
                        <div className="text-xs text-gray-500">
                          <p>Total citations: {critique.citation_network_analysis.citation_patterns.total_citations}</p>
                          <p>Density: {critique.citation_network_analysis.citation_patterns.citation_density} per 1000 words</p>
                          <p>Recent citations: {(critique.citation_network_analysis.citation_patterns.recent_citations_ratio * 100).toFixed(1)}%</p>
                        </div>
                      </div>

                      {/* Impact Assessment */}
                      <div className="border border-gray-200 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 mb-2">Impact Assessment</h3>
                        <div className={`inline-flex items-center px-2 py-1 rounded text-sm font-medium ${getScoreColor(critique.citation_network_analysis.impact_assessment.score)} mb-2`}>
                          {critique.citation_network_analysis.impact_assessment.score.toFixed(1)}/100
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{critique.citation_network_analysis.impact_assessment.assessment}</p>
                        <div className="text-xs text-gray-500">
                          <p>High-impact citations: {critique.citation_network_analysis.impact_assessment.high_impact_citations}</p>
                          <p>Citation diversity: {critique.citation_network_analysis.impact_assessment.citation_diversity}</p>
                          <p>Impact ratio: {critique.citation_network_analysis.impact_assessment.impact_ratio}</p>
                        </div>
                      </div>

                      {/* Cross-reference Validation */}
                      <div className="border border-gray-200 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 mb-2">Cross-references</h3>
                        <div className={`inline-flex items-center px-2 py-1 rounded text-sm font-medium ${getScoreColor(critique.citation_network_analysis.cross_reference_validation.score)} mb-2`}>
                          {critique.citation_network_analysis.cross_reference_validation.score}/100
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{critique.citation_network_analysis.cross_reference_validation.assessment}</p>
                        <div className="text-xs text-gray-500">
                          <p>Total internal refs: {critique.citation_network_analysis.cross_reference_validation.total_internal_references}</p>
                          <p>Tables: {critique.citation_network_analysis.cross_reference_validation.table_references}</p>
                          <p>Figures: {critique.citation_network_analysis.cross_reference_validation.figure_references}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* 4. Literature Analysis */}
              {critique.literature_analysis && (
                <div className="bg-white rounded-lg shadow">
                  <div className="p-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-6">
                      📚 Literature Analysis
                      <span className={`ml-4 inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(critique.literature_analysis.overall_literature_score)}`}>
                        {critique.literature_analysis.overall_literature_score.toFixed(1)}/100
                      </span>
                    </h2>
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <div className="border border-gray-200 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 mb-2">Gap Detection</h3>
                        <div className={`inline-flex items-center px-2 py-1 rounded text-sm font-medium ${getScoreColor(critique.literature_analysis.research_gaps.score)} mb-2`}>
                          {critique.literature_analysis.research_gaps.score}/100
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{critique.literature_analysis.research_gaps.assessment}</p>
                      </div>
                      <div className="border border-gray-200 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 mb-2">Novelty Assessment</h3>
                        <div className={`inline-flex items-center px-2 py-1 rounded text-sm font-medium ${getScoreColor(critique.literature_analysis.novelty_assessment.score)} mb-2`}>
                          {critique.literature_analysis.novelty_assessment.score}/100
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{critique.literature_analysis.novelty_assessment.assessment}</p>
                      </div>
                      <div className="border border-gray-200 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 mb-2">Research Positioning</h3>
                        <div className={`inline-flex items-center px-2 py-1 rounded text-sm font-medium ${getScoreColor(critique.literature_analysis.research_positioning.score)} mb-2`}>
                          {critique.literature_analysis.research_positioning.score}/100
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{critique.literature_analysis.research_positioning.assessment}</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* 5. Advanced Critique Features */}
              {critique.advanced_critique_features && (
                <div className="bg-white rounded-lg shadow">
                  <div className="p-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-6">
                      🔬 Advanced Critique Features
                      <span className={`ml-4 inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(critique.advanced_critique_features.overall_advanced_score)}`}>
                        {critique.advanced_critique_features.overall_advanced_score.toFixed(1)}/100
                      </span>
                    </h2>
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <div className="border border-gray-200 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 mb-2">Reproducibility</h3>
                        <div className={`inline-flex items-center px-2 py-1 rounded text-sm font-medium ${getScoreColor(critique.advanced_critique_features.reproducibility_assessment.score)} mb-2`}>
                          {critique.advanced_critique_features.reproducibility_assessment.score}/100
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{critique.advanced_critique_features.reproducibility_assessment.assessment}</p>
                      </div>
                      <div className="border border-gray-200 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 mb-2">Peer Review Quality</h3>
                        <div className={`inline-flex items-center px-2 py-1 rounded text-sm font-medium ${getScoreColor(critique.advanced_critique_features.peer_review_metrics.score)} mb-2`}>
                          {critique.advanced_critique_features.peer_review_metrics.score}/100
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{critique.advanced_critique_features.peer_review_metrics.assessment}</p>
                      </div>
                      <div className="border border-gray-200 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 mb-2">Reference Format</h3>
                        <div className={`inline-flex items-center px-2 py-1 rounded text-sm font-medium ${getScoreColor(critique.advanced_critique_features.reference_format_validation.score)} mb-2`}>
                          {critique.advanced_critique_features.reference_format_validation.score.toFixed(1)}/100
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{critique.advanced_critique_features.reference_format_validation.assessment}</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Academic Recommendations */}
              {critique.academic_recommendations && critique.academic_recommendations.length > 0 && (
                <div className="bg-white rounded-lg shadow">
                  <div className="p-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">
                      💡 Academic Recommendations
                    </h2>
                    <div className="space-y-3">
                      {critique.academic_recommendations.map((recommendation: string, index: number) => (
                        <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                          <div className="flex-shrink-0">
                            <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center">
                              <svg className="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd\"/>
                              </svg>
                            </div>
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm text-gray-900">{recommendation}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

        {/* Action Buttons */}
        <div className="mt-8 flex justify-center space-x-4">
          <button
            onClick={() => navigate('/')}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Analyze Another Document
          </button>
          <button
            onClick={() => {
              const dataStr = JSON.stringify(results, null, 2);
              const dataBlob = new Blob([dataStr], { type: 'application/json' });
              const url = URL.createObjectURL(dataBlob);
              const link = document.createElement('a');
              link.href = url;
              link.download = 'analysis-results.json';
              link.click();
              URL.revokeObjectURL(url);
            }}
            className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors font-medium"
          >
            Download Results
          </button>
        </div>
      </div>
    </div>
  );
};

export default Results;