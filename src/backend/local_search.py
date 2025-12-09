from typing import Any, Dict, List, Optional, Tuple
import math

def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Khoảng cách Haversine (km)."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def _iter_locations(data: Any) -> List[Dict[str, Any]]:
    """
    Chuẩn hóa dữ liệu đầu vào thành list[dict] có thể đọc:
    - Nếu data là dict và có khóa 'items' (accommodations.json), dùng data['items'].
    - Nếu data là list (accommodations list), dùng trực tiếp.
    - Ngược lại, trả về [].
    """
    if isinstance(data, dict):
        items = data.get("items")
        if isinstance(items, list):
            return items
        # Một số file có 'accommodations' thay vì 'items'
        accs = data.get("accommodations")
        if isinstance(accs, list):
            return accs
        return []
    if isinstance(data, list):
        return data
    return []

def find_nearest_location(lat: float, lon: float, data: Any) -> Optional[Dict[str, Any]]:
    """
    Tìm accommodation gần nhất làm đại diện 'location' (beach/province) cho bộ lọc.
    Hỗ trợ dữ liệu accommodations dạng list hoặc dict có 'items'/'accommodations'.
    """
    locations = _iter_locations(data)
    best: Tuple[float, Dict[str, Any]] = (float("inf"), {})
    for item in locations:
        # Bỏ qua phần tử không phải dict
        if not isinstance(item, dict):
            continue
        loc_lat = item.get("lat")
        loc_lon = item.get("lon")
        if not isinstance(loc_lat, (int, float)) or not isinstance(loc_lon, (int, float)):
            continue
        dist = _haversine_km(lat, lon, float(loc_lat), float(loc_lon))
        if dist < best[0]:
            best = (dist, item)
    return best[1] if best[0] != float("inf") else None

def extract_location_keys(location_item: Dict[str, Any]) -> Dict[str, Optional[str]]:
    """
    Trả về beach_key/province_key từ item gần nhất; fallback id/name nếu thiếu.
    """
    if not isinstance(location_item, dict):
        return {"beach_key": None, "province_key": None, "id": None, "name": None}
    return {
        "beach_key": location_item.get("beach_key"),
        "province_key": location_item.get("province_key"),
        "id": location_item.get("id"),
        "name": location_item.get("name"),
    }

# Ví dụ dùng trong search_accommodations:
# nearest = find_nearest_location(user_lat, user_lon, data)
# loc_keys = extract_location_keys(nearest)
# beach_key = loc_keys["beach_key"]
# province_key = loc_keys["province_key"]