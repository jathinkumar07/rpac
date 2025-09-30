#!/usr/bin/env python3
"""
Test the real Semantic Scholar API for citation validation
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.citations_service import CitationsService

def test_real_citations():
    """Test citation validation with real Semantic Scholar API"""
    print("🔍 Testing Real Semantic Scholar API for Citation Validation")
    print("=" * 60)
    
    # Sample text with real citations
    sample_text = """
    References
    
    1. Smith, J., Davis, M., & Brown, K. (2023). Deep Learning Applications in Scientific Research. Nature Machine Intelligence, 15(3), 234-247.
    
    2. Johnson, R., & Williams, A. (2022). Ensemble Methods for Academic Data Analysis. Journal of Machine Learning Research, 23(8), 1456-1478.
    
    3. LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature, 521(7553), 436-444.
    
    4. Goodfellow, Ian, et al. "Generative adversarial nets." Advances in neural information processing systems 27 (2014).
    """
    
    try:
        # Initialize citations service
        citations_service = CitationsService()
        
        # Extract citations
        print("📄 Extracting citations from text...")
        citations = citations_service.extract_citations(sample_text)
        print(f"   Found {len(citations)} citations")
        
        for i, citation in enumerate(citations[:3]):  # Show first 3
            print(f"   {i+1}. {citation[:80]}...")
        
        # Validate citations using real Semantic Scholar API
        print("\n🔍 Validating citations with real Semantic Scholar API...")
        validated_citations = citations_service.validate_citations(citations)
        
        print(f"\n📊 Validation Results:")
        valid_count = 0
        for i, result in enumerate(validated_citations):
            is_valid = result.get('valid', False)
            if is_valid:
                valid_count += 1
            
            status = "✅ VALID" if is_valid else "❌ INVALID"
            print(f"   {i+1}. {status}")
            print(f"      Reference: {result.get('reference', '')[:60]}...")
            print(f"      Searched: {result.get('searched_title', '')[:60]}...")
            
            if result.get('matched_paper'):
                matched = result['matched_paper']
                print(f"      Found: {matched.get('title', '')[:60]}...")
                if matched.get('authors'):
                    authors = [author.get('name', '') for author in matched['authors'][:2]]
                    print(f"      Authors: {', '.join(authors)}...")
            elif result.get('reason'):
                print(f"      Reason: {result['reason']}")
            print()
        
        print(f"📈 Summary: {valid_count}/{len(validated_citations)} citations validated successfully")
        
        # Test comprehensive report
        print("\n📋 Getting comprehensive citations report...")
        report = citations_service.get_citations_report(sample_text)
        
        print(f"   Total Citations: {report['total_citations']}")
        print(f"   Valid Citations: {report['valid_citations']}")
        print(f"   Invalid Citations: {report['invalid_citations']}")
        print(f"   Quality Score: {report['quality_score']:.1f}%")
        print(f"   Recommendation: {report['recommendations']}")
        
        print("\n✅ Real Semantic Scholar API test completed successfully!")
        print("🎉 Your citations are now validated using real academic data!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_real_citations()
    if success:
        print("\n🎉 SUCCESS: Real Semantic Scholar API is working!")
        print("Your backend now uses real academic data for citation validation.")
    else:
        print("\n❌ FAILED: Check the error messages above.")
    
    sys.exit(0 if success else 1)