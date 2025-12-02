"""
Pattern 4: Build Search Request
Tổng hợp thông tin thành SearchRequest object
"""

from typing import Dict
from config. settings import DEFAULT_SEARCH_RADIUS, MAX_RESULTS


def build_search_request(geo_data: Dict, filters: Dict) -> Dict:
    """
    Tổng hợp tất cả thông tin thành SearchRequest object
    
    Args:
        geo_data: Dữ liệu địa lý từ geocoding
        filters: Filters đã được normalize
    
    Returns:
        Dict chứa đầy đủ thông tin để search
    """
    return {
        'location_name': geo_data['name'],
        'lat': geo_data['lat'],
        'lon': geo_data['lon'],
        'budget': filters['budget'],
        'type': filters['type'],
        'tags': filters['tags'],
        'radius': DEFAULT_SEARCH_RADIUS,
        'max_results': MAX_RESULTS
    }