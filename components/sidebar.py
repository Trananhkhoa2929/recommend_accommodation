"""
Sidebar Component
"""

import streamlit as st


def render_sidebar(user_id: str):
    """
    Render sidebar với menu và user info
    
    Args:
        user_id: ID của user hiện tại
    """
    with st.sidebar:
        st. markdown("## 🏖️ Beach Finder")
        st.markdown("---")
        
        st.markdown("### 📍 Menu")
        st.markdown("""
        - 🏠 **Home** - Trang chủ
        - 🔍 **Search** - Tìm kiếm
        - 📜 **History** - Lịch sử
        - ℹ️ **About** - Giới thiệu
        """)
        
        st. markdown("---")
        
        st.markdown("### 🔧 User Info")
        st.code(f"ID: {user_id}")
        
        st.markdown("---")
        st.caption("Đồ án TDTT - Năm 2 | 2025")