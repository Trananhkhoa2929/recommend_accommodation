"""
History Page - Trang lịch sử tìm kiếm
"""

import streamlit as st
import uuid
from datetime import datetime

# Config
from config.styles import CUSTOM_CSS

# Services
from src import firebase_service

# ============================================================================
# PAGE SETUP
# ============================================================================

st.set_page_config(
    page_title="📜 Lịch sử - Beach Finder",
    page_icon="📜",
    layout="wide"
)
st. markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div class='history-header'>
    <h1>📜 Lịch sử tìm kiếm</h1>
    <p>Xem lại các địa điểm bạn đã tìm kiếm trước đó</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 🆔 User Info")
    st.code(f"ID: {st.session_state. user_id}")
    
    st.markdown("---")
    
    if st.button("🗑️ Xóa toàn bộ lịch sử", use_container_width=True):
        if firebase_service.clear_all_history(st.session_state.user_id):
            st.success("✅ Đã xóa!")
            st.rerun()
        else:
            st.warning("Không thể xóa hoặc chưa có lịch sử")

# ============================================================================
# CHECK FIREBASE
# ============================================================================

if not firebase_service.enabled:
    st.warning("""
    ⚠️ **Firebase chưa được cấu hình**
    
    Để sử dụng tính năng lưu lịch sử, vui lòng:
    
    1. Tạo project Firebase tại [console.firebase.google.com](https://console.firebase.google. com)
    2. Vào **Build** → **Realtime Database** → **Create Database**
    3. Chọn **Start in test mode**
    4.  Copy URL database
    5. Thêm vào file `.env`:
    
    ```
    FIREBASE_DATABASE_URL=https://your-project-id.firebaseio.com
    ```
    """)
    st. stop()

# ============================================================================
# LOAD & DISPLAY HISTORY
# ============================================================================

history = firebase_service.get_search_history(st.session_state. user_id, limit=20)

if not history:
    st.markdown("""
    <div class='empty-state'>
        <div class='empty-icon'>📭</div>
        <h3>Chưa có lịch sử tìm kiếm</h3>
        <p>Hãy bắt đầu tìm kiếm nơi ở để lưu lại lịch sử! </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("👈 Chọn **🔍 Search** từ menu bên trái để bắt đầu tìm kiếm")

else:
    st.markdown(f"### 📊 Tổng cộng: {len(history)} lần tìm kiếm")
    
    for entry in history:
        # Parse timestamp
        try:
            timestamp = datetime.fromisoformat(entry. get('timestamp', ''))
            date_str = timestamp.strftime("%d/%m/%Y %H:%M")
        except:
            date_str = "N/A"
        
        # Display card
        st.markdown(f"""
        <div class='history-card'>
            <div class='history-date'>🕐 {date_str}</div>
            <div class='history-location'>🌊 {entry.get('search_query', 'N/A')}</div>
            <div style='margin-top: 0. 5rem;'>
                <span class='history-tag'>💰 {entry.get('budget', 'N/A')}</span>
                <span class='history-tag'>🏠 {entry.get('type', 'N/A')}</span>
                <span class='history-tag'>📊 {entry.get('results_count', 0)} kết quả</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show top results in expander
        top_results = entry.get('top_results', [])
        if top_results:
            with st.expander("👀 Xem kết quả đề xuất"):
                for i, result in enumerate(top_results, 1):
                    st. markdown(f"""
                    **#{i} {result. get('name', 'N/A')}**  
                    Loại: {result.get('type', 'N/A')} | 
                    Điểm: {result.get('score', 0)} | 
                    Khoảng cách: {result. get('distance', 'N/A')}
                    """)
        
        # Delete button
        entry_id = entry.get('id', '')
        if entry_id:
            if st.button(f"🗑️ Xóa", key=f"del_{entry_id}"):
                if firebase_service.delete_history_entry(st.session_state. user_id, entry_id):
                    st.rerun()
        
        st.markdown("---")