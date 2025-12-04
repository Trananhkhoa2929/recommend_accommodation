"""
About Page - Trang giới thiệu
"""

import streamlit as st

# Config
from config.styles import CUSTOM_CSS

# ============================================================================
# PAGE SETUP
# ============================================================================

st.set_page_config(
    page_title="ℹ️ Giới thiệu - Beach Finder",
    page_icon="ℹ️",
    layout="wide"
)
st. markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st. markdown("""
<div class='about-header'>
    <h1>ℹ️ Giới thiệu</h1>
    <p>Đồ án Tư duy Tính toán - Năm 2</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# PROJECT INFO
# ============================================================================

st. markdown("### 📚 Thông tin Dự án")

col1, col2 = st. columns(2)

with col1:
    st.markdown("""
    | Thông tin | Chi tiết |
    |-----------|----------|
    | **Đồ án** | Tư duy Tính toán |
    | **Năm** | Năm 2 |
    | **Tác giả** | Trananhkhoa2929 |
    | **Ngày tạo** | 11/11/2025 |
    | **Cập nhật** | 02/12/2025 |
    """)

with col2:
    st.markdown("""
    | Repository | Link |
    |------------|------|
    | **GitHub** | [AI_recommend_accommodation](https://github.com/Trananhkhoa2929/AI_recommend_accommodation) |
    | **Demo** | Streamlit App |
    | **License** | MIT |
    """)

# ============================================================================
# 4 PILLARS OF COMPUTATIONAL THINKING
# ============================================================================

st.markdown("### 🎯 4 Trụ cột Tư duy Tính toán")

p_col1, p_col2 = st.columns(2)

with p_col1:
    st.markdown("""
    <div class='pillar-card'>
        <div class='pillar-number'>01</div>
        <h4>Problem Analysis</h4>
        <p style='font-size: 0.9rem;'>Phân tích bài toán: Người dùng cần tìm nơi ở gần biển 
        nhưng không biết địa điểm cụ thể, không muốn mất thời gian duyệt qua hàng trăm kết quả.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='pillar-card'>
        <div class='pillar-number'>02</div>
        <h4>Decomposition</h4>
        <p style='font-size: 0.9rem;'>Chia nhỏ bài toán: Input cleaning → Geocoding → 
        Searching → Filtering → Ranking.  Nhận diện pattern lặp lại trong việc xử lý dữ liệu địa lý.</p>
    </div>
    """, unsafe_allow_html=True)

with p_col2:
    st.markdown("""
    <div class='pillar-card'>
        <div class='pillar-number'>03</div>
        <h4>Abstraction</h4>
        <p style='font-size: 0.9rem;'>Trừu tượng hóa: Tạo các module độc lập 
        (input, backend, services, utils) để có thể tái sử dụng và bảo trì dễ dàng.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='pillar-card'>
        <div class='pillar-number'>04</div>
        <h4>Algorithm Design</h4>
        <p style='font-size: 0.9rem;'>Thiết kế thuật toán xếp hạng dựa trên: 
        khoảng cách (Haversine), độ khớp tags, loại hình nơi ở, và tên rõ ràng.</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# TECHNOLOGY STACK
# ============================================================================

st.markdown("### 🛠️ Công nghệ sử dụng")

t1, t2, t3, t4, t5 = st.columns(5)

techs = [
    ("🤖", "Gemini AI", "Làm sạch input"),
    ("🗺️", "OpenStreetMap", "Geocoding & Search"),
    ("🔥", "Firebase", "Lưu lịch sử"),
    ("🎨", "Streamlit", "Web Framework"),
    ("🐍", "Python", "Backend")
]

for col, (icon, name, desc) in zip([t1, t2, t3, t4, t5], techs):
    with col:
        st.markdown(f"""
        <div class='tech-card'>
            <div class='tech-icon'>{icon}</div>
            <h4>{name}</h4>
            <p style='font-size: 0.8rem; color: #666;'>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PROCESS FLOW
# ============================================================================

st.markdown("### 🔄 Quy trình xử lý")

steps = [
    ("Bước 1: AI Input Cleaning", "Gemini AI sửa lỗi chính tả, chuẩn hóa tên địa điểm"),
    ("Bước 2: Geocoding", "OpenStreetMap Nominatim API chuyển tên thành tọa độ GPS"),
    ("Bước 3: Normalize Filters", "Chuẩn hóa filters sang format OSM tags"),
    ("Bước 4: Search", "Overpass API tìm kiếm nơi ở trong bán kính 5km"),
    ("Bước 5: Filter & Rank", "Lọc theo tiêu chí, xếp hạng theo thuật toán scoring"),
    ("Bước 6: Save History", "Lưu kết quả vào Firebase Realtime Database")
]

for title, desc in steps:
    st.markdown(f"""
    <div class='process-step'>
        <strong>{title}</strong><br>
        <span style='color: #666;'>{desc}</span>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PROJECT STRUCTURE
# ============================================================================

st. markdown("### 📁 Cấu trúc dự án")

st.code("""
beach-accommodation-finder/
├── app. py                      # Main entry point
├── config/
│   ├── settings.py             # App settings
│   └── styles.py               # CSS styles
├── components/
│   ├── sidebar.py              # Sidebar UI
│   ├── hero.py                 # Hero section
│   ├── chat_bot.py             # Chat bot với USP
│   ├── features.py             # Feature cards
│   └── footer.py               # Footer
├── pages/
│   ├── 1_Search.py             # Search page
│   ├── 2_History.py            # History page
│   └── 3_About.py              # About page
└── src/
    ├── input/
    │   ├── ai_cleaning.py      # Pattern 1: AI cleaning
    │   ├── geocoding.py        # Pattern 2: Geocoding
    │   ├── normalizer.py       # Pattern 3: Normalize
    │   └── request_builder.py  # Pattern 4: Build request
    ├── backend/
    │   ├── osm_search.py       # Pattern 5: OSM search
    │   ├── data_normalizer.py  # Pattern 6: Normalize data
    │   ├── filter. py           # Pattern 7: Filter
    │   └── ranking. py          # Pattern 8: Ranking
    ├── services/
    │   └── firebase_service.py # Firebase integration
    └── utils/
        ├── distance. py         # Haversine distance
        └── formatters.py       # Format helpers
""", language="text")

# ============================================================================
# FOOTER
# ============================================================================

st. markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 1rem 0;'>
    <p>Made with ❤️ by Trananhkhoa2929</p>
    <p style='font-size: 0. 85rem;'>© 2025 - Đồ án Tư duy Tính toán</p>
</div>
""", unsafe_allow_html=True)