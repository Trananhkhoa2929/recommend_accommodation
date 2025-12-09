"""
Pattern 3: Normalize Input Filters
Chuẩn hóa các filter từ text sang giá trị chuẩn
- Mở rộng mapping cho budget/type/tags để bao quát dữ liệu trong accommodations.json
"""

from typing import Dict, List
import unicodedata
import re


def _strip_accents(text: str) -> str:
    """Bỏ dấu tiếng Việt để so khớp không phân biệt dấu."""
    if not text:
        return ""
    text = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in text if unicodedata.category(ch) != "Mn")


def _normalize_space(text: str) -> str:
    """Chuẩn hóa khoảng trắng, lower, bỏ ký tự thừa phổ biến."""
    if not text:
        return ""
    text = text.lower()
    # thay các ký tự phân tách phổ biến bằng khoảng trắng
    text = re.sub(r"[,\.;:/\\\|\-\(\)\[\]\{\}_]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Mapping ngân sách -> 3 bậc low/medium/high (giữ tương thích)
# Gợi ý: dữ liệu có price_level: budget/mid/upper_mid/luxury
# => Quy chiếu: budget -> low, mid -> medium, upper_mid|luxury -> high
BUDGET_MAP = {
    # VI
    "rẻ": "low",
    "giá rẻ": "low",
    "bình dân": "low",
    "giá mềm": "low",
    "tiết kiệm": "low",
    "trung bình": "medium",
    "bình thường": "medium",
    "phổ thông": "medium",
    "tầm trung": "medium",
    "trung cấp": "medium",
    "cao": "high",
    "đắt": "high",
    "cao cấp": "high",
    "sang": "high",
    "sang trọng": "high",
    "sang chảnh": "high",
    "thượng lưu": "high",
    # EN
    "cheap": "low",
    "budget": "low",
    "low": "low",
    "normal": "medium",
    "mid": "medium",
    "midrange": "medium",
    "mid-range": "medium",
    "medium": "medium",
    "upper mid": "high",
    "upper_mid": "high",
    "uppermid": "high",
    "premium": "high",
    "high": "high",
    "luxury": "high",
}

# Mapping loại hình -> dataset canonical: hotel | homestay | resort
TYPE_MAP = {
    # VI
    "khách sạn": "hotel",
    "ks": "hotel",
    "nhà nghỉ": "homestay",      # hoặc 'hostel' nếu bạn có type riêng
    "ký túc xá": "homestay",     # hoặc 'hostel'
    "homestay": "homestay",
    "căn hộ": "homestay",
    "chung cư": "homestay",
    "căn hộ dịch vụ": "homestay",
    "condotel": "homestay",
    "apartment": "homestay",
    "studio": "homestay",
    "resort": "resort",
    "khu nghỉ dưỡng": "resort",
    "biệt thự": "resort",        # gom villa vào resort cho đơn giản
    "villa": "resort",
    # EN
    "hotel": "hotel",
    "hostel": "homestay",        # hoặc để nguyên 'hostel' nếu có
    "guesthouse": "homestay",
    "guest house": "homestay",
    "residence": "homestay",
    "serviced apartment": "homestay",
}

# Mapping TAGS: gom về canonical tag như dataset đã dùng
# Ưu tiên cụm dài trước (sẽ sắp xếp khi duyệt)
TAG_MAP = {
    # Beach proximity / views
    "bãi biển riêng": "private_beach",
    "private beach": "private_beach",
    "sát biển": "beachfront",
    "ngay bờ biển": "beachfront",
    "beachfront": "beachfront",
    "gần biển": "near-beach",
    "near beach": "near-beach",
    "view biển": "sea-view",
    "hướng biển": "sea-view",
    "sea view": "sea-view",

    # Facilities
    "hồ bơi vô cực": "pool",
    "infinity pool": "pool",
    "hồ bơi": "pool",
    "bể bơi": "pool",
    "pool": "pool",
    "spa": "spa",
    "xông hơi": "sauna",
    "sauna": "sauna",
    "gym": "gym",
    "phòng gym": "gym",
    "fitness": "gym",
    "nhà hàng": "restaurant",
    "restaurant": "restaurant",
    "quán bar": "bar",
    "bar": "bar",
    "bãi đỗ xe": "parking",
    "chỗ đỗ xe": "parking",
    "parking": "parking",
    "wifi": "wifi",
    "wi fi": "wifi",
    "internet": "wifi",
    "buffet sáng": "breakfast",
    "bữa sáng": "breakfast",
    "breakfast": "breakfast",
    "phòng họp": "conference",
    "hội nghị": "conference",
    "conference": "conference",
    "xe đưa đón": "shuttle",
    "shuttle": "shuttle",
    "thang máy": "elevator",
    "elevator": "elevator",
    "máy giặt": "laundry",
    "giặt ủi": "laundry",
    "laundry": "laundry",

    # Family / kids
    "phù hợp gia đình": "family",
    "gia đình": "family",
    "family": "family",
    "trẻ em": "kids",
    "kids": "kids",
    "kids club": "kids_club",
    "kids-club": "kids_club",
    "câu lạc bộ trẻ em": "kids_club",

    # Style / ambiance
    "lãng mạn": "romantic",
    "romantic": "romantic",
    "yên tĩnh": "quiet",
    "quiet": "quiet",
    "sôi động": "lively",
    "náo nhiệt": "lively",
    "lively": "lively",
    "vibrant": "lively",
    "view đẹp": "scenic",
    "scenic": "scenic",
    "sạch sẽ": "clean",
    "sạch bóng": "clean",
    "clean": "clean",
    "mới sửa sang": "renovated",
    "mới được xây dựng": "renovated",
    "renovated": "renovated",
    "ban công": "balcony",
    "balcony": "balcony",

    # Room features for apts
    "bếp nhỏ": "kitchenette",
    "kitchenette": "kitchenette",
    "bếp": "kitchen",
    "kitchen": "kitchen",
    "căn hộ": "apartment",
    "apartment": "apartment",

    # Activities
    "lướt sóng": "surf",
    "lướt ván": "surf",
    "surf": "surf",
    "snorkel": "snorkel",
    "lặn ngắm san hô": "snorkel",
    "casino": "casino_nearby",
    "casino nearby": "casino_nearby",

    # Special/marketing flags
    "agoda preferred": "agoda_preferred",
    "giải thưởng 2024": "award_2024",
    "award 2024": "award_2024",
    "hủy miễn phí": "free_cancellation",
    "miễn phí hủy": "free_cancellation",
    "free cancellation": "free_cancellation",
    "không cần thẻ tín dụng": "no_credit_card",
    "no credit card": "no_credit_card",

    # Others
    "villa": "villa",
    "biệt thự": "villa",
    "hồ bơi riêng": "private_pool",
    "private pool": "private_pool",
    "thành phố": "city",
    "city": "city",
}


def _match_tags_free_text(text: str) -> List[str]:
    """
    Dò các cụm tag trong chuỗi tự do (không phân biệt dấu).
    Ưu tiên cụm dài hơn để tránh trùng khớp bán phần.
    """
    if not text or not text.strip():
        return []

    raw = _normalize_space(text)
    raw_no_acc = _strip_accents(raw)

    tags: List[str] = []
    # Sắp xếp key theo độ dài (desc) để ưu tiên cụm dài
    keys_sorted = sorted(TAG_MAP.keys(), key=lambda k: len(k), reverse=True)

    for key in keys_sorted:
        key_norm = _normalize_space(key)
        key_no_acc = _strip_accents(key_norm)
        if key_no_acc and key_no_acc in raw_no_acc:
            tag = TAG_MAP[key]
            if tag not in tags:
                tags.append(tag)

    return tags


def normalize_filters(budget_text: str, type_text: str, ambiance_text: str) -> Dict:
    """
    Chuẩn hóa các filter từ text sang giá trị chuẩn

    Args:
        budget_text: Mức giá (text). Ví dụ: 'rẻ', 'budget', 'mid', 'upper_mid', 'luxury', ...
        type_text: Loại hình (text). Ví dụ: 'khách sạn', 'homestay', 'condotel', 'villa', ...
        ambiance_text: Cụm mô tả/ưu tiên (text). Ví dụ: 'bãi biển riêng, hồ bơi, gia đình, yên tĩnh'

    Returns:
        Dict chứa các giá trị đã chuẩn hóa:
        {
          'budget': 'low|medium|high',
          'type': 'hotel|homestay|resort',
          'tags': [canonical_tag,...]
        }
    """
    # Normalize budget (fallback 'medium')
    bt = _normalize_space(budget_text or "")
    bt_no_acc = _strip_accents(bt)
    budget_tier = BUDGET_MAP.get(bt, None) or BUDGET_MAP.get(bt_no_acc, None) or "medium"

    # Normalize type (fallback 'homestay' cho trải nghiệm thân thiện)
    tt = _normalize_space(type_text or "")
    tt_no_acc = _strip_accents(tt)
    acc_type = TYPE_MAP.get(tt, None) or TYPE_MAP.get(tt_no_acc, None) or "homestay"

    # Normalize ambiance tags (free text, phrase matching)
    tags = _match_tags_free_text(ambiance_text or "")

    return {
        "budget": budget_tier,
        "type": acc_type,
        "tags": tags,
    }