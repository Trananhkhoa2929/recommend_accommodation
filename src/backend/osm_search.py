"""
Pattern 5: Local Data Search
Tìm kiếm từ dữ liệu local JSON thay vì API
"""

import json
import os
from typing import List, Dict, Optional, Tuple
from src.utils.distance import haversine_distance

# Path to data file
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'accommodations.json')


def load_data() -> Dict:
    """Load dữ liệu từ file JSON"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {DATA_FILE}")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Lỗi parse JSON: {e}")
        return {}


def find_nearest_location(lat: float, lon: float, data: Dict) -> Optional[str]:
    """
    Tìm địa điểm gần nhất với tọa độ cho trước
    
    Args:
        lat, lon: Tọa độ tìm kiếm
        data: Dữ liệu accommodations
    
    Returns:
        Key của địa điểm gần nhất (vd: 'vung_tau')
    """
    min_distance = float('inf')
    nearest_location = None
    
    for location_key, location_data in data.items():
        loc_lat = location_data.get('lat', 0)
        loc_lon = location_data.get('lon', 0)
        
        distance = haversine_distance(lat, lon, loc_lat, loc_lon)
        
        if distance < min_distance:
            min_distance = distance
            nearest_location = location_key
    
    # Chỉ trả về nếu khoảng cách < 50km
    if min_distance < 50:
        return nearest_location
    
    return None


def search_accommodations(search_request: Dict) -> Tuple[Optional[List], Optional[str]]:
    """
    Tìm kiếm nơi ở từ dữ liệu local
    
    Args:
        search_request: Dict chứa thông tin tìm kiếm
            - lat, lon: Tọa độ trung tâm
            - radius: Bán kính tìm kiếm (meters)
            - type: Loại nơi ở
            - tags: Tags mong muốn
            - budget: Mức giá
    
    Returns:
        Tuple (elements, error_message)
    """
    # Load data
    data = load_data()
    
    if not data:
        return None, "Không thể tải dữ liệu địa điểm"
    
    # Extract parameters
    lat = search_request['lat']
    lon = search_request['lon']
    radius_m = search_request.get('radius', 5000)
    radius_km = radius_m / 1000
    
    # Find nearest location
    location_key = find_nearest_location(lat, lon, data)
    
    if not location_key:
        return None, "Không tìm thấy địa điểm nào trong hệ thống gần vị trí này"
    
    location_data = data[location_key]
    accommodations = location_data.get('accommodations', [])
    
    if not accommodations:
        return None, f"Chưa có dữ liệu nơi ở cho {location_data.get('name', location_key)}"
    
    # Filter by distance
    results = []
    for acc in accommodations:
        acc_lat = acc.get('lat', 0)
        acc_lon = acc.get('lon', 0)
        
        distance = haversine_distance(lat, lon, acc_lat, acc_lon)
        
        if distance <= radius_km:
            # Convert to element format (compatible with normalize function)
            element = {
                'id': acc.get('id', ''),
                'lat': acc_lat,
                'lon': acc_lon,
                'tags': {
                    'name': acc.get('name', 'Unnamed'),
                    'tourism': acc.get('type', 'hotel'),
                    'price_level': acc.get('price_level', 'medium'),
                    'rating': acc.get('rating', 0),
                    'reviews': acc.get('reviews', 0),
                    'address': acc.get('address', ''),
                    'phone': acc.get('phone', ''),
                    'website': acc.get('website', ''),
                    'description': acc.get('description', ''),
                    'amenities': acc.get('amenities', []),
                    'custom_tags': acc.get('tags', []),
                    'source': 'local'
                }
            }
            results.append(element)
    
    if not results:
        return None, f"Không tìm thấy nơi ở nào trong bán kính {radius_km}km"
    
    return results, None


def get_supported_locations() -> List[Dict]:
    """
    Lấy danh sách các địa điểm được hỗ trợ
    
    Returns:
        List các địa điểm với name, lat, lon
    """
    data = load_data()
    
    locations = []
    for key, value in data.items():
        locations.append({
            'key': key,
            'name': value.get('name', key),
            'lat': value.get('lat', 0),
            'lon': value.get('lon', 0),
            'count': len(value.get('accommodations', []))
        })
    
    return locations


def get_all_tags() -> List[str]:
    """Lấy tất cả tags có trong dữ liệu"""
    data = load_data()
    
    all_tags = set()
    for location_data in data.values():
        for acc in location_data.get('accommodations', []):
            tags = acc.get('tags', [])
            all_tags.update(tags)
    
    return sorted(list(all_tags))