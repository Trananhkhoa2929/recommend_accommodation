"""
Pattern 1: AI Input Cleaning
Sử dụng Gemini API để làm sạch và chuẩn hóa tên địa điểm
"""

import json
from typing import Tuple, Optional, Dict
import google.generativeai as genai


def clean_location_input(raw_text: str, api_key: str) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Sử dụng Gemini API để làm sạch và phân tích input địa điểm
    
    Args:
        raw_text: Văn bản thô người dùng nhập
        api_key: Gemini API key
    
    Returns:
        Tuple (parsed_data, error_message)
        - parsed_data: Dict chứa province_name, beach_name (nếu có)
        - error_message: Thông báo lỗi nếu có
    """
    if not raw_text or raw_text.strip() == "":
        return None, "Input không được để trống"
    
    if not api_key:
        return None, "Chưa cấu hình GEMINI_API_KEY"
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        prompt = f"""Bạn là trợ lý phân tích địa danh biển Việt Nam. 

User nhập: "{raw_text}"

Nhiệm vụ:
1. Sửa lỗi chính tả (nếu có)
2.  Nhận diện TỈNH/THÀNH PHỐ (province)
3. Nhận diện BÃI BIỂN cụ thể (beach) nếu user có đề cập

Quy tắc:
- "VungTau", "vung tau" → province: "Vũng Tàu"
- "bãi sau vũng tàu" → province: "Vũng Tàu", beach: "Bãi Sau"
- "nha trang" → province: "Nha Trang"
- "mỹ khê đà nẵng" → province: "Đà Nẵng", beach: "Mỹ Khê"
- Nếu chỉ có tên biển không rõ tỉnh, cố gắng suy luận

Trả về CHÍNH XÁC theo format JSON (không có markdown):
{{"province": "Tên Tỉnh", "beach": "Tên Bãi Biển hoặc null", "original": "input gốc"}}

Ví dụ:
Input: "bãi sau vt" → {{"province": "Vũng Tàu", "beach": "Bãi Sau", "original": "bãi sau vt"}}
Input: "nhatrang" → {{"province": "Nha Trang", "beach": null, "original": "nhatrang"}}
Input: "mỹ khê" → {{"province": "Đà Nẵng", "beach": "Mỹ Khê", "original": "mỹ khê"}}

Trả về JSON:"""

        response = model.generate_content(prompt)
        
        if not response or not response.text:
            return None, "Gemini API không trả về kết quả"
        
        # Parse JSON response
        response_text = response.text.strip()
        
        # Remove markdown code block if present
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1])
        
        parsed = json.loads(response_text)
        
        if not parsed.get('province'):
            return None, "Không thể nhận diện địa điểm"
        
        return parsed, None
        
    except json.JSONDecodeError:
        return None, "Không thể phân tích response từ AI"
    except Exception as e:
        return None, f"Lỗi khi gọi Gemini API: {str(e)}"