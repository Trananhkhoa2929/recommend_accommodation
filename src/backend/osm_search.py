"""
Pattern 5: Searching
OpenStreetMap Overpass API Search
"""

import time
import requests
from typing import List, Dict, Optional, Tuple


# Overpass API servers (fallback)
OVERPASS_SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass. kumi.systems/api/interpreter",
    "https://overpass. openstreetmap.ru/api/interpreter"
]


def search_accommodations(search_request: Dict) -> Tuple[Optional[List], Optional[str]]:
    """
    Tìm kiếm nơi ở bằng OpenStreetMap Overpass API với retry và fallback
    
    Args:
        search_request: Dict chứa thông tin tìm kiếm
    
    Returns:
        Tuple (osm_elements, error_message)
    """
    # Extract parameters
    lat = search_request['lat']
    lon = search_request['lon']
    acc_type = search_request['type']
    radius = search_request['radius']
    
    # Expand tourism types for better results
    tourism_types = [acc_type, 'hotel', 'guest_house', 'apartment', 'hostel']
    types_regex = "|".join(tourism_types)
    
    # Build Overpass query
    query = f"""
    [out:json][timeout:20];
    (
      node["tourism"~"^({types_regex})$"](around:{radius},{lat},{lon});
      way["tourism"~"^({types_regex})$"](around:{radius},{lat},{lon});
    );
    out body 50;
    """
    
    last_error = None
    
    # Try each server
    for server_url in OVERPASS_SERVERS:
        try:
            response = requests.post(
                server_url,
                data={'data': query},
                timeout=25,
                headers={'User-Agent': 'BeachAccommodationFinder/2.0'}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if 'elements' in data and len(data['elements']) > 0:
                    return data['elements'], None
                else:
                    last_error = f"Server {server_url. split('/')[2]} không có kết quả"
                    continue
            
            elif response.status_code in [504, 429]:
                last_error = f"Server {server_url.split('/')[2]} quá tải"
                time.sleep(2)
                continue
            
            else:
                last_error = f"HTTP {response.status_code}"
                continue
                
        except requests.exceptions.Timeout:
            last_error = f"Server {server_url.split('/')[2]} timeout"
            continue
        
        except requests.exceptions.RequestException as e:
            last_error = f"Lỗi kết nối: {str(e)}"
            continue
        
        except Exception as e:
            last_error = f"Lỗi: {str(e)}"
            continue
    
    return None, f"Không thể kết nối Overpass API.  {last_error}"