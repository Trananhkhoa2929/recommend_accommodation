"""
Pattern 2: Validation + Geocoding
Sử dụng OpenStreetMap Nominatim API
"""

import time
import requests
from typing import Tuple, Dict, Optional


def validate_and_geocode(location_name: str) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Xác thực địa điểm và lấy tọa độ GPS từ OpenStreetMap
    
    Args:
        location_name: Tên địa điểm đã được làm sạch
    
    Returns:
        Tuple (geo_data, error_message)
        - Nếu thành công: (geo_data_dict, None)
        - Nếu lỗi: (None, error_message)
    """
    try:
        # Nominatim API URL
        url = "https://nominatim.openstreetmap.org/search"
        
        # Parameters
        params = {
            'q': f"{location_name}, Vietnam",
            'format': 'json',
            'limit': 1,
            'addressdetails': 1
        }
        
        # Headers (required by Nominatim)
        headers = {
            'User-Agent': 'BeachAccommodationFinder/2.0 (Educational Project)'
        }
        
        # Rate limit delay
        time.sleep(1)
        
        # Make request
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        # Check status
        if response.status_code != 200:
            return None, f"Nominatim API trả về lỗi: {response.status_code}"
        
        # Parse JSON
        data = response.json()
        
        # Check results
        if not data or len(data) == 0:
            return None, f"Không tìm thấy địa điểm '{location_name}' ở Việt Nam"
        
        # Get first result
        result = data[0]
        
        # Build geo_data
        geo_data = {
            'name': result.get('display_name', location_name),
            'lat': float(result['lat']),
            'lon': float(result['lon']),
            'type': result.get('type', 'unknown'),
            'importance': result.get('importance', 0)
        }
        
        return geo_data, None
        
    except requests.exceptions.Timeout:
        return None, "Timeout khi gọi Nominatim API (quá 10s)"
    except requests.exceptions.RequestException as e:
        return None, f"Lỗi kết nối Nominatim API: {str(e)}"
    except Exception as e:
        return None, f"Lỗi không xác định: {str(e)}"