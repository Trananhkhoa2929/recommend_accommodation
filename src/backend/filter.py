"""
Pattern 7: Filter Results
Lọc các kết quả theo criteria
"""

from typing import List, Dict
from src.utils.distance import haversine_distance


def filter_results(accommodations: List[Dict], search_request: Dict) -> List[Dict]:
    """
    Lọc các kết quả theo criteria
    
    Args:
        accommodations: List các Accommodation objects
        search_request: Search request chứa filters
    
    Returns:
        List các Accommodation đã lọc
    """
    filtered = []
    
    center_lat = search_request['lat']
    center_lon = search_request['lon']
    max_distance = search_request['radius'] / 1000  # Convert m to km
    required_tags = search_request.get('tags', [])
    
    for acc in accommodations:
        # Calculate distance
        acc_lat, acc_lon = acc['location']
        distance = haversine_distance(center_lat, center_lon, acc_lat, acc_lon)
        
        # Filter 1: Distance
        if distance > max_distance:
            continue
        
        # Filter 2: Tags (if required)
        if required_tags:
            has_match = any(tag in acc['tags'] for tag in required_tags)
            if not has_match:
                continue
        
        # Pass all filters
        acc['distance'] = distance
        filtered.append(acc)
    
    return filtered