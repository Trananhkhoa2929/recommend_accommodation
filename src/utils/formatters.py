"""
Formatting Utilities
"""


def format_distance(distance_km: float) -> str:
    """
    Format khoảng cách để hiển thị
    
    Args:
        distance_km: Khoảng cách tính bằng km
    
    Returns:
        String đã format (vd: "2.5 km" hoặc "850 m")
    """
    if distance_km < 1:
        return f"{int(distance_km * 1000)} m"
    return f"{distance_km:.1f} km"