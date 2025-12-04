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
    required_budget = search_request.get('budget', 'medium')
    
    # Budget mapping
    budget_map = {
        'low': ['low'],
        'medium': ['low', 'medium'],
        'high': ['medium', 'high']
    }
    acceptable_budgets = budget_map.get(required_budget, ['low', 'medium', 'high'])
    
    for acc in accommodations:
        score = 10.0  # Base score
        
        # Component 1: Proximity score (closer = higher, max 5 points)
        distance = acc.get('distance', 0)
        if distance > 0:
            proximity_score = max(0, 5 - distance)
        else:
            proximity_score = 5
        score += proximity_score
        
        # Component 2: Rating score (max 5 points)
        rating = acc.get('rating', 0)
        if rating > 0:
            rating_score = rating  # 0-5 points
            score += rating_score
        
        # Component 3: Reviews bonus (more reviews = more trusted)
        reviews = acc.get('reviews', 0)
        if reviews > 1000:
            score += 2
        elif reviews > 500:
            score += 1.5
        elif reviews > 100:
            score += 1
        elif reviews > 0:
            score += 0.5
        
        # Component 4: Tag match score (max 6 points)
        acc_tags = set(acc.get('tags', []))
        required_tags_set = set(required_tags)
        tag_matches = len(acc_tags & required_tags_set)
        tag_score = tag_matches * 2
        score += tag_score
        
        # Component 5: Type bonus
        if acc.get('type') == search_request.get('type'):
            score += 2
        
        # Component 6: Budget match
        acc_budget = acc.get('price_level', 'medium')
        if acc_budget in acceptable_budgets:
            score += 1
        
        # Component 7: Name bonus (has clear name)
        if acc.get('name', 'Unnamed') != 'Unnamed':
            score += 0.5
        
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