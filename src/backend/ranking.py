"""
Pattern 8: Ranking
Xếp hạng các kết quả theo score
"""

from typing import List, Dict
from config.settings import TOP_RESULTS_COUNT


def rank_results(accommodations: List[Dict], search_request: Dict) -> List[Dict]:
    """
    Xếp hạng các kết quả theo score
    
    Args:
        accommodations: List các Accommodation đã lọc
        search_request: Search request để tính bonus
    
    Returns:
        List các Accommodation đã xếp hạng (top N)
    """
    if not accommodations:
        return []
    
    required_tags = search_request.get('tags', [])
    
    for acc in accommodations:
        score = 10.0  # Base score
        
        # Component 1: Proximity score (closer = higher)
        distance = acc['distance']
        proximity_score = max(0, 5 - distance)
        score += proximity_score
        
        # Component 2: Tag match score
        acc_tags = set(acc['tags'])
        required_tags_set = set(required_tags)
        tag_matches = len(acc_tags & required_tags_set)
        tag_score = tag_matches * 2
        score += tag_score
        
        # Component 3: Type bonus (exact match)
        if acc['type'] == search_request['type']:
            score += 3
        
        # Component 4: Name bonus (has clear name)
        if acc['name'] != 'Unnamed':
            score += 1
        
        # Assign score
        acc['score'] = round(score, 2)
    
    # Sort by score descending
    sorted_accs = sorted(accommodations, key=lambda x: x['score'], reverse=True)
    
    # Get top results
    top_results = sorted_accs[:TOP_RESULTS_COUNT]
    
    # Add rank
    for i, acc in enumerate(top_results):
        acc['rank'] = i + 1
    
    return top_results