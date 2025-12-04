"""
Pattern 6: Normalize Output
Chuyển đổi dữ liệu sang Accommodation objects
Hỗ trợ dữ liệu local JSON
"""

from typing import List, Dict


def normalize_osm_data(elements: List[Dict]) -> List[Dict]:
    """
    Chuyển đổi dữ liệu từ search sang cấu trúc Accommodation chuẩn
    
    Args:
        elements: List các elements từ search
    
    Returns:
        List các Accommodation objects (dạng dict)
    """
    accommodations = []
    seen_names = set()
    
    for element in elements:
        if 'tags' not in element:
            continue
        
        tags = element['tags']
        
        # Extract name
        name = tags.get('name', 'Unnamed')
        
        # Skip duplicates
        if name in seen_names:
            continue
        
        # Must have coordinates
        if 'lat' not in element or 'lon' not in element:
            continue
        
        lat = element['lat']
        lon = element['lon']
        
        # Extract type
        tourism_type = tags.get('tourism', 'hotel')
        
        # Build tags list từ custom_tags
        acc_tags = tags.get('custom_tags', [tourism_type])
        if tourism_type not in acc_tags:
            acc_tags.insert(0, tourism_type)
        
        # Extra info
        price_level = tags.get('price_level', 'medium')
        rating = tags.get('rating', 0)
        reviews = tags.get('reviews', 0)
        address = tags.get('address', '')
        phone = tags.get('phone', '')
        website = tags.get('website', '')
        description = tags.get('description', '')
        amenities = tags.get('amenities', [])
        source = tags.get('source', 'local')
        
        # Build Accommodation object
        accommodation = {
            'id': element.get('id', ''),
            'name': name,
            'location': (lat, lon),
            'type': tourism_type,
            'tags': acc_tags,
            'price_level': price_level,
            'rating': rating,
            'reviews': reviews,
            'address': address,
            'phone': phone,
            'website': website,
            'description': description,
            'amenities': amenities,
            'source': source,
            'score': 0.0,
            'distance': 0.0
        }
        
        accommodations.append(accommodation)
        seen_names.add(name)
    
    return accommodations