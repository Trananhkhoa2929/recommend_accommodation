"""
Pattern 3: Normalize Input Filters
Chuẩn hóa các filter từ text sang giá trị chuẩn
"""

from typing import Dict, List


# Mapping dictionaries
BUDGET_MAP = {
    'rẻ': 'low',
    'giá rẻ': 'low',
    'cheap': 'low',
    'bình thường': 'medium',
    'trung bình': 'medium',
    'normal': 'medium',
    'cao': 'high',
    'đắt': 'high',
    'sang trọng': 'high',
    'luxury': 'high'
}

TYPE_MAP = {
    'homestay': 'guest_house',
    'nhà nghỉ': 'guest_house',
    'khách sạn': 'hotel',
    'hotel': 'hotel',
    'resort': 'resort',
    'villa': 'chalet',
    'biệt thự': 'chalet',
    'hostel': 'hostel',
    'ký túc xá': 'hostel'
}

AMBIANCE_MAP = {
    'yên tĩnh': 'quiet',
    'quiet': 'quiet',
    'peaceful': 'quiet',
    'sôi động': 'lively',
    'lively': 'lively',
    'vibrant': 'lively',
    'gần biển': 'beachfront',
    'beach': 'beachfront',
    'beachfront': 'beachfront',
    'view đẹp': 'scenic',
    'scenic': 'scenic',
    'gia đình': 'family',
    'family': 'family',
    'romantic': 'romantic',
    'lãng mạn': 'romantic'
}


def normalize_filters(budget_text: str, type_text: str, ambiance_text: str) -> Dict:
    """
    Chuẩn hóa các filter từ text sang giá trị chuẩn
    
    Args:
        budget_text: Mức giá (text)
        type_text: Loại hình (text)
        ambiance_text: Cảm giác mong muốn (text)
    
    Returns:
        Dict chứa các giá trị đã chuẩn hóa
    """
    # Normalize budget
    budget_tier = BUDGET_MAP.get(budget_text.lower(). strip(), 'medium')
    
    # Normalize type
    acc_type = TYPE_MAP.get(type_text.lower().strip(), 'guest_house')
    
    # Normalize ambiance tags
    tags: List[str] = []
    if ambiance_text and ambiance_text.strip():
        words = [w.strip() for w in ambiance_text.replace(',', ' ').split()]
        for word in words:
            tag = AMBIANCE_MAP.get(word.lower())
            if tag and tag not in tags:
                tags.append(tag)
    
    return {
        'budget': budget_tier,
        'type': acc_type,
        'tags': tags
    }