"""
Pattern 2: Beach Dictionary Lookup
Tra cứu từ điển bãi biển theo tỉnh/thành
"""

import json
import os
from typing import Dict, List, Optional, Tuple

# Path to dictionary file
DICT_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'beaches_dictionary.json')


def load_dictionary() -> Dict:
    """Load từ điển bãi biển"""
    try:
        with open(DICT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {DICT_FILE}")
        return {"provinces": {}}
    except json.JSONDecodeError as e:
        print(f"❌ Lỗi parse JSON: {e}")
        return {"provinces": {}}


def normalize_text(text: str) -> str:
    """Chuẩn hóa text để so sánh"""
    return text.lower().strip()


def find_province(province_name: str) -> Tuple[Optional[str], Optional[Dict]]:
    """
    Tìm province trong từ điển
    
    Args:
        province_name: Tên tỉnh từ Gemini
    
    Returns:
        Tuple (province_key, province_data) hoặc (None, None)
    """
    data = load_dictionary()
    provinces = data.get('provinces', {})
    
    normalized_input = normalize_text(province_name)
    
    for key, province_data in provinces.items():
        # Check exact name
        if normalize_text(province_data.get('name', '')) == normalized_input:
            return key, province_data
        
        # Check aliases
        aliases = province_data.get('aliases', [])
        for alias in aliases:
            if normalize_text(alias) == normalized_input:
                return key, province_data
    
    return None, None


def find_beach_in_province(beach_name: str, province_data: Dict) -> Optional[Dict]:
    """
    Tìm bãi biển cụ thể trong tỉnh
    
    Args:
        beach_name: Tên bãi biển
        province_data: Dữ liệu tỉnh
    
    Returns:
        Beach data hoặc None
    """
    if not beach_name:
        return None
    
    beaches = province_data.get('beaches', [])
    normalized_input = normalize_text(beach_name)
    
    for beach in beaches:
        # Check exact name
        if normalize_text(beach.get('name', '')) == normalized_input:
            return beach
        
        # Check aliases
        aliases = beach.get('aliases', [])
        for alias in aliases:
            if normalize_text(alias) == normalized_input:
                return beach
    
    return None


class BeachLookupResult:
    """Kết quả tra cứu từ điển"""
    
    # Status codes
    NOT_FOUND = "not_found"              # Không tìm thấy tỉnh
    NO_BEACH = "no_beach"                # Tỉnh không có biển
    SINGLE_BEACH = "single_beach"        # Tỉnh chỉ có 1 biển
    MULTIPLE_BEACHES = "multiple_beaches" # Tỉnh có nhiều biển
    BEACH_SELECTED = "beach_selected"    # Đã xác định được biển cụ thể
    
    def __init__(self):
        self.status = None
        self.province_key = None
        self.province_name = None
        self.province_data = None
        self.beach = None
        self.beaches = []
        self.message = ""


def lookup_beach(parsed_input: Dict) -> BeachLookupResult:
    """
    Tra cứu từ điển bãi biển
    
    Args:
        parsed_input: Dict từ Gemini với keys: province, beach
    
    Returns:
        BeachLookupResult với status và data
    """
    result = BeachLookupResult()
    
    province_name = parsed_input.get('province')
    beach_name = parsed_input.get('beach')
    
    if not province_name:
        result.status = BeachLookupResult.NOT_FOUND
        result.message = "Không thể xác định địa điểm"
        return result
    
    # Find province
    province_key, province_data = find_province(province_name)
    
    if not province_data:
        result.status = BeachLookupResult.NOT_FOUND
        result.message = f"Không tìm thấy '{province_name}' trong hệ thống"
        return result
    
    result.province_key = province_key
    result.province_name = province_data.get('name')
    result.province_data = province_data
    
    # Check if province has beach
    if not province_data.get('has_beach', False):
        result.status = BeachLookupResult.NO_BEACH
        result.message = province_data.get('message', f"{result.province_name} không có bãi biển")
        return result
    
    beaches = province_data.get('beaches', [])
    result.beaches = beaches
    
    # If user specified a beach, try to find it
    if beach_name:
        found_beach = find_beach_in_province(beach_name, province_data)
        if found_beach:
            result.status = BeachLookupResult.BEACH_SELECTED
            result.beach = found_beach
            result.message = f"Đã chọn: {found_beach.get('name')} - {result.province_name}"
            return result
    
    # Check number of beaches
    if len(beaches) == 1:
        result.status = BeachLookupResult.SINGLE_BEACH
        result.beach = beaches[0]
        result.message = f"Có phải bạn muốn tìm nơi ở tại {beaches[0].get('name')} - {result.province_name}?"
    else:
        result.status = BeachLookupResult.MULTIPLE_BEACHES
        result.message = f"{result.province_name} có {len(beaches)} bãi biển.  Bạn muốn tìm ở bãi nào?"
    
    return result


def get_all_provinces() -> List[Dict]:
    """Lấy danh sách tất cả tỉnh có biển"""
    data = load_dictionary()
    provinces = data.get('provinces', {})
    
    result = []
    for key, province_data in provinces.items():
        if province_data.get('has_beach', False):
            result.append({
                'key': key,
                'name': province_data.get('name'),
                'beach_count': len(province_data.get('beaches', []))
            })
    
    return result