"""
Features & Stats Components
"""

import streamlit as st


def render_features():
    """Render feature cards"""
    
    st. markdown("### 🎯 Tính năng nổi bật")
    
    col1, col2, col3, col4 = st.columns(4)
    
    features = [
        ("🤖", "AI Gemini", "Hiểu ngữ cảnh và sửa lỗi thông minh"),
        ("🗺️", "OpenStreetMap", "Dữ liệu thực, cập nhật liên tục"),
        ("📊", "Smart Ranking", "Xếp hạng thông minh theo tiêu chí"),
        ("🔥", "Firebase Sync", "Lưu lịch sử đám mây")
    ]
    
    for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
        with col:
            st.markdown(f"""
            <div class='feature-card'>
                <div class='feature-icon'>{icon}</div>
                <h4>{title}</h4>
                <p style='font-size: 0.85rem; color: #666;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)


def render_stats():
    """Render statistics section"""
    
    st.markdown("### 📈 Thống kê")
    
    col1, col2, col3 = st.columns(3)
    
    stats = [
        ("63+", "Tỉnh thành Việt Nam"),
        ("∞", "Địa điểm trên OSM"),
        ("100%", "Miễn phí")
    ]
    
    for col, (number, label) in zip([col1, col2, col3], stats):
        with col:
            st.markdown(f"""
            <div class='stat-box'>
                <div class='stat-number'>{number}</div>
                <div class='stat-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)