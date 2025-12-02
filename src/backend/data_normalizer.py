"""
Pattern 6: Normalize Output
Chuyển đổi dữ liệu OSM sang Accommodation objects
"""

from typing import List, Dict


def normalize_osm_data(osm_elements: List[Dict]) -> List[Dict]:
    """
    Chuyển đổi dữ liệu thô từ OSM sang cấu trúc Accommodation chuẩn
    
    Args:
        osm_elements: List các elements từ OSM Overpass
    
    Returns:
        List các Accommodation objects (dạng dict)
    """
    accommodations = []
    seen_names = set()  # Avoid duplicates
    
    for element in osm_elements:
        # Skip elements without tags
        if 'tags' not in element:
            continue
        
        tags = element['tags']
        
        # Extract name
        name = tags.get('name', tags.get('addr:street', 'Unnamed'))
        
        # Skip duplicates
        if name in seen_names:
            continue
        
        # Must have coordinates
        if 'lat' not in element or 'lon' not in element:
            continue
        
        lat = element['lat']
        lon = element['lon']
        
        # Extract tourism type
        tourism_type = tags.get('tourism', 'accommodation')
        
        # Build tags list
        acc_tags = [tourism_type]
        
        if 'amenity' in tags:
            acc_tags.append(tags['amenity'])
        if 'building' in tags:
            acc_tags.append(tags['building'])
        
        # Build Accommodation object
        accommodation = {
            'id': element. get('id', 0),
            'name': name,
            'location': (lat, lon),
            'type': tourism_type,
            'tags': acc_tags,
            'score': 0.0,
            'distance': 0.0,
            'source': 'osm'
        }
        
        accommodations. append(accommodation)
        seen_names.add(name)
    
    return accommodations