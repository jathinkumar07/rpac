#!/usr/bin/env python3
"""
Create a sample PDF for testing the analysis endpoint.
"""

from reportlab.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

def create_sample_pdf():
    """Create a sample research paper PDF for testing."""
    output_path = "uploads/sample.pdf"
    
    # Ensure uploads directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Create PDF document
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Add content
    title = Paragraph("Machine Learning in Academic Research: A Comprehensive Analysis", title_style)
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Abstract
    abstract_style = styles['Normal']
    abstract = Paragraph("<b>Abstract</b><br/><br/>This paper presents a comprehensive analysis of machine learning applications in academic research. We surveyed 500 research papers and found that 78% of studies reported significant improvements using ML techniques. Our findings demonstrate the effectiveness of various algorithms in different domains.", abstract_style)
    story.append(abstract)
    story.append(Spacer(1, 20))
    
    # Introduction
    intro = Paragraph("<b>1. Introduction</b><br/><br/>Machine learning has revolutionized academic research across multiple disciplines. Smith et al. (2023) demonstrated that neural networks achieve 95% accuracy in classification tasks. Johnson and Williams (2022) further showed that ensemble methods provide robust performance across diverse datasets.", abstract_style)
    story.append(intro)
    story.append(Spacer(1, 20))
    
    # Methodology
    methodology = Paragraph("<b>2. Methodology</b><br/><br/>We conducted a systematic review of machine learning applications in academic research. Our analysis included papers from 2020-2024, focusing on reproducibility and statistical significance. Data was collected from PubMed, IEEE Xplore, and ACM Digital Library databases.", abstract_style)
    story.append(methodology)
    story.append(Spacer(1, 20))
    
    # Results
    results = Paragraph("<b>3. Results</b><br/><br/>Our analysis revealed significant trends in ML adoption. Random forests achieved the highest accuracy (92.3%) in classification tasks, while deep learning models excelled in image recognition with 97.8% accuracy. Statistical analysis showed p < 0.001 for all major findings.", abstract_style)
    story.append(results)
    story.append(Spacer(1, 20))
    
    # References
    references = Paragraph("<b>References</b><br/><br/>1. Smith, J., Davis, M., & Brown, K. (2023). Deep Learning Applications in Scientific Research. Nature Machine Intelligence, 15(3), 234-247.<br/><br/>2. Johnson, R., & Williams, A. (2022). Ensemble Methods for Academic Data Analysis. Journal of Machine Learning Research, 23(8), 1456-1478.<br/><br/>3. Chen, L., et al. (2024). Statistical Significance in ML-Based Research Studies. Science, 380(6648), 123-129.", abstract_style)
    story.append(references)
    
    # Build PDF
    doc.build(story)
    print(f"✅ Sample PDF created: {output_path}")
    return output_path

if __name__ == "__main__":
    create_sample_pdf()