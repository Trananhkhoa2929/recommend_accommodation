"""
Predefined prompts and allowed questions for Q&A
"""

# Danh sách câu hỏi được phép
ALLOWED_QUESTIONS = {
    "why_recommend": {
        "patterns": [
            "tại sao",
            "vì sao",
            "lý do",
            "why",
            "recommend",
            "đề xuất",
            "gợi ý"
        ],
        "display": "🤔 Tại sao lại đề xuất nơi này?"
    },
    "compare": {
        "patterns": [
            "so sánh",
            "compare",
            "khác gì",
            "khác nhau",
            "hơn"
        ],
        "display": "⚖️ So sánh các kết quả"
    },
    "more_info": {
        "patterns": [
            "thông tin thêm",
            "chi tiết",
            "detail",
            "more info",
            "tell me more"
        ],
        "display": "📋 Thông tin chi tiết về nơi này"
    },
    "nearby": {
        "patterns": [
            "gần đó",
            "nearby",
            "xung quanh",
            "lân cận",
            "quanh đây"
        ],
        "display": "📍 Có gì xung quanh khu vực này?"
    },
    "price": {
        "patterns": [
            "giá",
            "price",
            "bao nhiêu",
            "chi phí",
            "cost"
        ],
        "display": "💰 Thông tin về giá cả"
    },
    "best_time": {
        "patterns": [
            "thời điểm",
            "khi nào",
            "mùa",
            "season",
            "best time"
        ],
        "display": "🗓️ Thời điểm tốt nhất để đi?"
    }
}


def get_system_prompt(search_data: dict, results: list) -> str:
    """
    Tạo system prompt cho Gemini dựa trên dữ liệu tìm kiếm
    
    Args:
        search_data: Thông tin tìm kiếm của user
        results: Kết quả đề xuất
    
    Returns:
        System prompt string
    """
    
    # Format results for prompt
    results_text = ""
    for i, r in enumerate(results[:5], 1):
        results_text += f"""
        #{i}.{r.get('name', 'N/A')}
        - Loại: {r.get('type', 'N/A')}
        - Rating: {r.get('rating', 0)}/5 ({r.get('reviews', 0)} đánh giá)
        - Khoảng cách: {r.get('distance', 0):.2f} km
        - Điểm hệ thống: {r.get('score', 0)}/30
        - Tags: {', '.join(r.get('tags', []))}
        - Mức giá: {r.get('price_level', 'N/A')}
        - Địa chỉ: {r.get('address', 'N/A')}
        """
    
    return f"""Bạn là trợ lý AI của hệ thống Beach Accommodation Finder.

## THÔNG TIN TÌM KIẾM CỦA USER:
- Địa điểm: {search_data.get('location', 'N/A')}
- Bãi biển: {search_data.get('beach_name', 'N/A')}
- Mức giá mong muốn: {search_data.get('budget', 'N/A')}
- Loại nơi ở: {search_data.get('type', 'N/A')}
- Không khí: {search_data.get('ambiance', 'N/A')}
- Tags: {', '.join(search_data.get('tags', []))}

## KẾT QUẢ ĐỀ XUẤT:
{results_text}

## QUY TẮC TRẢ LỜI:
1. CHỈ trả lời dựa trên dữ liệu được cung cấp ở trên
2.  KHÔNG bịa thông tin không có trong dữ liệu
3.  Trả lời ngắn gọn, đúng trọng tâm (tối đa 200 từ)
4.  Sử dụng tiếng Việt, thân thiện
5. Nếu được hỏi về giá cụ thể mà không có data, nói "Vui lòng liên hệ trực tiếp khách sạn"
6. Giải thích rõ TẠI SAO hệ thống đề xuất dựa trên:
   - Độ khớp với yêu cầu (tags, loại, mức giá)
   - Rating và số lượng đánh giá
   - Khoảng cách đến trung tâm bãi biển
"""


def get_why_recommend_prompt(top_result: dict, search_data: dict) -> str:
    """Prompt giải thích tại sao recommend"""
    return f"""Giải thích ngắn gọn tại sao hệ thống đề xuất "{top_result.get('name')}" là lựa chọn #1:

Yêu cầu của user:
- Mức giá: {search_data.get('budget', 'N/A')}
- Loại: {search_data.get('type', 'N/A')}
- Tags mong muốn: {', '.join(search_data.get('tags', []))}

Thông tin nơi ở:
- Rating: {top_result.get('rating', 0)}/5
- Số đánh giá: {top_result.get('reviews', 0)}
- Khoảng cách: {top_result.get('distance', 0):.2f} km
- Tags: {', '.join(top_result.get('tags', []))}
- Điểm hệ thống: {top_result.get('score', 0)}

Hãy giải thích bằng 3-4 bullet points."""


def get_compare_prompt(results: list) -> str:
    """Prompt so sánh các kết quả"""
    comparison = ""
    for r in results[:3]:
        comparison += f"- {r.get('name')}: {r.get('rating', 0)}⭐, {r.get('price_level', 'N/A')}, {r.get('distance', 0):.1f}km\n"
    
    return f"""So sánh ngắn gọn 3 lựa chọn hàng đầu:

{comparison}

Đưa ra bảng so sánh đơn giản và kết luận nên chọn cái nào trong trường hợp nào."""


def match_question(user_input: str) -> tuple:
    """
    Kiểm tra input có khớp với câu hỏi được phép không
    
    Args:
        user_input: Câu hỏi của user
    
    Returns:
        Tuple (question_key, is_allowed)
    """
    normalized = user_input.lower().strip()
    
    for key, question_data in ALLOWED_QUESTIONS.items():
        patterns = question_data.get('patterns', [])
        for pattern in patterns:
            if pattern in normalized:
                return key, True
    
    return None, False


def get_allowed_questions_display() -> list:
    """Lấy danh sách câu hỏi được phép để hiển thị"""
    return [q['display'] for q in ALLOWED_QUESTIONS.values()]