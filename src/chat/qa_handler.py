"""
Q&A Handler - Xử lý hỏi đáp sau khi có kết quả
"""

from typing import Dict, List, Optional, Tuple
import google.generativeai as genai
from .prompts import (
    get_system_prompt,
    get_why_recommend_prompt,
    get_compare_prompt,
    match_question,
    get_allowed_questions_display,
    ALLOWED_QUESTIONS
)


class QAHandler:
    """Handler cho Q&A với Gemini"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.chat_history = []
        self.search_data = {}
        self.results = []
        self.is_initialized = False
        
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-2.5-flash")
        else:
            self.model = None
    
    def initialize(self, search_data: Dict, results: List[Dict]):
        """
        Khởi tạo context cho Q&A
        
        Args:
            search_data: Dữ liệu tìm kiếm
            results: Kết quả đề xuất
        """
        self.search_data = search_data
        self.results = results
        self.chat_history = []
        self.is_initialized = True
        
        # Lưu system prompt
        self.system_prompt = get_system_prompt(search_data, results)
    
    def get_suggested_questions(self) -> List[str]:
        """Lấy danh sách câu hỏi gợi ý"""
        return get_allowed_questions_display()
    
    def process_question(self, user_question: str) -> Tuple[str, bool]:
        """
        Xử lý câu hỏi của user
        
        Args:
            user_question: Câu hỏi
        
        Returns:
            Tuple (answer, is_valid_question)
        """
        if not self.is_initialized:
            return "Vui lòng thực hiện tìm kiếm trước khi hỏi.", False
        
        if not self.model:
            return "Chưa cấu hình API key.", False
        
        # Check if question is allowed
        question_key, is_allowed = match_question(user_question)
        
        if not is_allowed:
            suggestions = "\n".join([f"  • {q}" for q in self.get_suggested_questions()])
            return f"""⚠️ Xin lỗi, tôi chỉ có thể trả lời các câu hỏi liên quan đến kết quả tìm kiếm. 

📝 Bạn có thể hỏi:
{suggestions}""", False
        
        # Generate specific prompt based on question type
        try:
            if question_key == "why_recommend":
                if self.results:
                    specific_prompt = get_why_recommend_prompt(self.results[0], self.search_data)
                else:
                    return "Không có kết quả để giải thích.", False
                    
            elif question_key == "compare":
                if len(self.results) < 2:
                    return "Cần ít nhất 2 kết quả để so sánh.", False
                specific_prompt = get_compare_prompt(self.results)
                
            else:
                # Generic question
                specific_prompt = f"User hỏi: {user_question}"
            
            # Call Gemini with system prompt + specific prompt
            full_prompt = f"""{self.system_prompt}

---
USER HỎI: {user_question}

{specific_prompt}

Trả lời:"""

            response = self.model.generate_content(full_prompt)
            
            if response and response.text:
                answer = response.text.strip()
                
                # Save to history
                self.chat_history.append({
                    'role': 'user',
                    'content': user_question
                })
                self.chat_history.append({
                    'role': 'assistant',
                    'content': answer
                })
                
                return answer, True
            else:
                return "Không thể tạo câu trả lời.", False
                
        except Exception as e:
            return f"Lỗi: {str(e)}", False
    
    def get_chat_history(self) -> List[Dict]:
        """Lấy lịch sử chat"""
        return self.chat_history
    
    def clear_history(self):
        """Xóa lịch sử chat"""
        self.chat_history = []