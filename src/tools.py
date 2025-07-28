from typing import List, Dict
from ddgs import DDGS


def search_web(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Search DuckDuckGo for information"""
    try:
        ddgs = DDGS()
        results = []
        
        for result in ddgs.text(query, max_results=max_results):
            results.append({
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "snippet": result.get("body", "")
            })
        
        return results
    except Exception as e:
        print(f"Search error: {e}")
        return []