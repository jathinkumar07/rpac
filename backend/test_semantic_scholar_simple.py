#!/usr/bin/env python3
"""
Simple test to verify Semantic Scholar API is working
"""

import requests
import json

def test_semantic_scholar_direct():
    """Test Semantic Scholar API directly"""
    print("🔍 Testing Semantic Scholar API directly...")
    
    # Test with a well-known paper
    search_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": "Deep learning",
        "fields": "title,authors,year",
        "limit": 3
    }
    
    try:
        response = requests.get(search_url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Working! Found {len(data.get('data', []))} papers")
            
            for i, paper in enumerate(data.get('data', [])[:2]):
                print(f"\n{i+1}. {paper.get('title', 'No title')}")
                authors = paper.get('authors', [])
                if authors:
                    author_names = [author.get('name', 'Unknown') for author in authors[:3]]
                    print(f"   Authors: {', '.join(author_names)}")
                print(f"   Year: {paper.get('year', 'Unknown')}")
            
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    success = test_semantic_scholar_direct()
    if success:
        print("\n🎉 Semantic Scholar API is working!")
        print("✅ Your backend will now use REAL citation data!")
    else:
        print("\n❌ API test failed. Check your internet connection.")