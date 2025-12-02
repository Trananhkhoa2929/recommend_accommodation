"""
Pattern 1: AI Input Cleaning
Sử dụng Gemini API để làm sạch và sửa lỗi tên địa điểm
"""

from typing import Tuple, Optional
import google.generativeai as genai


def clean_location_input(raw_text: str, api_key: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Sử dụng Gemini API để làm sạch và sửa lỗi tên địa điểm
    
    Args:
        raw_text: Văn bản thô người dùng nhập
        api_key: Gemini API key
    
    Returns:
        Tuple (cleaned_text, error_message)
        - Nếu thành công: (cleaned_text, None)
        - Nếu lỗi: (None, error_message)
    """
    # Validate input
    if not raw_text or raw_text.strip() == "":
        return None, "Input không được để trống"
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Build prompt
        prompt = f"""Bạn là trợ lý sửa lỗi địa danh Việt Nam. 

User nhập: "{raw_text}"

Nhiệm vụ:
1. Sửa lỗi chính tả nếu có
2. Chuẩn hóa tên địa điểm (viết hoa đúng)
3. Nếu là tên bãi biển nổi tiếng ở Việt Nam, trả về tên đầy đủ

Chỉ trả về TÊN ĐỊA ĐIỂM đã sửa, không giải thích gì thêm. 

Ví dụ:
- "vung tau" → "Vũng Tàu"
- "nha trang" → "Nha Trang"
- "da nang" → "Đà Nẵng"

Trả về:"""

        # Call API
        response = model.generate_content(prompt)
        
        # Validate response
        if not response or not response.text:
            return None, "Gemini API không trả về kết quả"
        
        cleaned = response.text.strip()
        
        # Validate cleaned text
        if len(cleaned) < 2 or len(cleaned) > 100:
            return None, "Tên địa điểm không hợp lệ"
        
        return cleaned, None
        
    except Exception as e:
        return None, f"Lỗi khi gọi Gemini API: {str(e)}"