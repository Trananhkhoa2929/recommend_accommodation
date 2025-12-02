"""
Firebase Service
Lưu và quản lý lịch sử tìm kiếm với Firebase Realtime Database
"""

import requests
from datetime import datetime
from typing import List, Dict
from config.settings import FIREBASE_DATABASE_URL


class FirebaseService:
    """Service để tương tác với Firebase Realtime Database"""
    
    def __init__(self):
        """Khởi tạo Firebase service"""
        self.database_url = FIREBASE_DATABASE_URL
        self.enabled = bool(self.database_url)
    
    def save_search_history(self, user_id: str, search_data: Dict) -> bool:
        """
        Lưu lịch sử tìm kiếm vào Firebase
        
        Args:
            user_id: ID định danh người dùng
            search_data: Dữ liệu tìm kiếm cần lưu
        
        Returns:
            True nếu lưu thành công
        """
        if not self.enabled:
            return False
        
        try:
            history_entry = {
                'timestamp': datetime.now().isoformat(),
                'search_query': search_data. get('location', ''),
                'cleaned_query': search_data.get('cleaned_location', ''),
                'budget': search_data.get('budget', ''),
                'type': search_data.get('type', ''),
                'ambiance': search_data.get('ambiance', ''),
                'results_count': search_data.get('results_count', 0),
                'top_results': search_data.get('top_results', [])[:3]
            }
            
            url = f"{self.database_url}/history/{user_id}. json"
            response = requests.post(url, json=history_entry, timeout=10)
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Firebase error: {str(e)}")
            return False
    
    def get_search_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Lấy lịch sử tìm kiếm từ Firebase
        
        Args:
            user_id: ID định danh người dùng
            limit: Số lượng kết quả tối đa
        
        Returns:
            List các history entries
        """
        if not self.enabled:
            return []
        
        try:
            url = f"{self.database_url}/history/{user_id}.json"
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            
            if not data:
                return []
            
            # Convert dict to list
            history_list = []
            for key, value in data.items():
                if isinstance(value, dict):
                    value['id'] = key
                    history_list.append(value)
            
            # Sort by timestamp descending
            history_list.sort(key=lambda x: x. get('timestamp', ''), reverse=True)
            
            return history_list[:limit]
            
        except Exception:
            return []
    
    def delete_history_entry(self, user_id: str, entry_id: str) -> bool:
        """Xóa một entry lịch sử"""
        if not self.enabled:
            return False
        
        try:
            url = f"{self.database_url}/history/{user_id}/{entry_id}.json"
            response = requests.delete(url, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def clear_all_history(self, user_id: str) -> bool:
        """Xóa toàn bộ lịch sử của user"""
        if not self.enabled:
            return False
        
        try:
            url = f"{self.database_url}/history/{user_id}.json"
            response = requests.delete(url, timeout=10)
            return response.status_code == 200
        except:
            return False


# Singleton instance
firebase_service = FirebaseService()