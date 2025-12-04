"""
Search Page - Trang tìm kiếm nơi ở
Với hệ thống Dictionary Lookup và Smart Q&A
"""

import streamlit as st
import uuid

# Config
from config.settings import GEMINI_API_KEY
from config.styles import CUSTOM_CSS

# Input Processing
from src.input import (
    clean_location_input,
    lookup_beach,
    BeachLookupResult,
    normalize_filters,
    build_search_request
)

# Backend
from src.backend import (
    search_accommodations,
    normalize_osm_data,
    filter_results,
    rank_results
)

# Utils
from src.utils.formatters import format_distance

# Services
from src.services.firebase_service import firebase_service

# Chat
from src.chat import QAHandler, get_allowed_questions_display

# ============================================================================
# PAGE SETUP
# ============================================================================

st.set_page_config(
    page_title="🔍 Tìm kiếm - Beach Finder",
    page_icon="🔍",
    layout="wide"
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]

if 'search_step' not in st.session_state:
    st.session_state.search_step = 'input'  # input, select_beach, confirm_beach, searching, results, qa

if 'parsed_input' not in st.session_state:
    st.session_state.parsed_input = None

if 'lookup_result' not in st.session_state:
    st.session_state.lookup_result = None

if 'selected_beach' not in st.session_state:
    st.session_state.selected_beach = None

if 'search_results' not in st.session_state:
    st.session_state.search_results = None

if 'search_data' not in st.session_state:
    st.session_state.search_data = {}

if 'qa_handler' not in st.session_state:
    st.session_state.qa_handler = QAHandler(GEMINI_API_KEY)

if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def reset_search():
    """Reset về bước đầu"""
    st.session_state.search_step = 'input'
    st.session_state.parsed_input = None
    st.session_state.lookup_result = None
    st.session_state.selected_beach = None
    st.session_state.search_results = None
    st.session_state.search_data = {}
    st.session_state.chat_messages = []

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div class='search-header'>
    <h1>🔍 Tìm kiếm nơi ở ven biển</h1>
    <p>Nhập địa điểm để bắt đầu tìm kiếm</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# STEP 1: INPUT
# ============================================================================

if st.session_state.search_step == 'input':
    st.markdown("### 📍 Bước 1: Nhập địa điểm")
    
    with st.form("location_form"):
        location_input = st.text_input(
            "Nhập tên bãi biển hoặc tỉnh/thành",
            placeholder="Ví dụ: Vũng Tàu, bãi sau, Nha Trang, mỹ khê đà nẵng..."
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            budget_input = st.selectbox("💰 Mức giá", ["trung bình", "rẻ", "cao", "sang trọng"])
        with col2:
            type_input = st.selectbox("🏨 Loại nơi ở", ["hotel", "homestay", "resort", "hostel", "villa"])
        with col3:
            radius_km = st.slider("📏 Bán kính (km)", 1, 20, 5)
        
        ambiance_input = st.text_input(
            "🎯 Không khí mong muốn (tùy chọn)",
            placeholder="yên tĩnh, gần biển, view đẹp..."
        )
        
        submitted = st.form_submit_button("🔍 Tìm kiếm", use_container_width=True)
    
    if submitted:
        if not location_input.strip():
            st.warning("⚠️ Vui lòng nhập địa điểm!")
        elif not GEMINI_API_KEY:
            st.error("❌ Chưa cấu hình GEMINI_API_KEY")
        else:
            with st.spinner("🤖 AI đang phân tích..."):
                # Step 1: Gemini normalize
                parsed, error = clean_location_input(location_input, GEMINI_API_KEY)
                
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.session_state.parsed_input = parsed
                    st.session_state.search_data = {
                        'location': location_input,
                        'budget': budget_input,
                        'type': type_input,
                        'radius_km': radius_km,
                        'ambiance': ambiance_input
                    }
                    
                    # Step 2: Dictionary lookup
                    lookup_result = lookup_beach(parsed)
                    st.session_state.lookup_result = lookup_result
                    
                    if lookup_result.status == BeachLookupResult.NOT_FOUND:
                        st.error(f"❌ {lookup_result.message}")
                        
                    elif lookup_result.status == BeachLookupResult.NO_BEACH:
                        st.warning(f"🏔️ {lookup_result.message}")
                        st.info("👆 Vui lòng nhập lại địa điểm khác")
                        
                    elif lookup_result.status == BeachLookupResult.BEACH_SELECTED:
                        st.session_state.selected_beach = lookup_result.beach
                        st.session_state.search_step = 'searching'
                        st.rerun()
                        
                    elif lookup_result.status == BeachLookupResult.SINGLE_BEACH:
                        st.session_state.search_step = 'confirm_beach'
                        st.rerun()
                        
                    elif lookup_result.status == BeachLookupResult.MULTIPLE_BEACHES:
                        st.session_state.search_step = 'select_beach'
                        st.rerun()
# ============================================================================
# STEP 2A: SELECT BEACH (Multiple beaches)
# ============================================================================

elif st.session_state.search_step == 'select_beach':
    lookup_result = st.session_state.lookup_result
    
    st.markdown(f"### 🏖️ {lookup_result.province_name} có {len(lookup_result.beaches)} bãi biển")
    st.markdown("**Vui lòng chọn bãi biển bạn muốn tìm nơi ở:**")
    
    cols = st.columns(2)
    for i, beach in enumerate(lookup_result.beaches):
        with cols[i % 2]:
            if st.button(
                f"🏖️ {beach['name']}\n\n{beach.get('description', '')}",
                key=f"beach_{beach['key']}",
                use_container_width=True
            ):
                st.session_state.selected_beach = beach
                st.session_state.search_step = 'searching'
                st.rerun()
    
    st.markdown("---")
    if st.button("⬅️ Quay lại", use_container_width=True):
        reset_search()
        st.rerun()

# ============================================================================
# STEP 2B: CONFIRM BEACH (Single beach)
# ============================================================================

elif st.session_state.search_step == 'confirm_beach':
    lookup_result = st.session_state.lookup_result
    beach = lookup_result.beach
    
    st.markdown(f"### ✅ Xác nhận địa điểm")
    
    st.info(f"""
    **{beach['name']}** - {lookup_result.province_name}
    
    📝 {beach.get('description', '')}
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Đúng, tìm kiếm", type="primary", use_container_width=True):
            st.session_state.selected_beach = beach
            st.session_state.search_step = 'searching'
            st.rerun()
    with col2:
        if st.button("❌ Không, nhập lại", use_container_width=True):
            reset_search()
            st.rerun()

# ============================================================================
# STEP 3: SEARCHING
# ============================================================================

elif st.session_state.search_step == 'searching':
    beach = st.session_state.selected_beach
    search_data = st.session_state.search_data
    lookup_result = st.session_state.lookup_result
    
    st.markdown(f"### 🔍 Đang tìm kiếm tại {beach['name']}...")
    
    with st.spinner("Đang xử lý..."):
        # Normalize filters
        filters = normalize_filters(
            search_data['budget'],
            search_data['type'],
            search_data['ambiance']
        )
        
        # Build search request
        geo_data = {
            'name': f"{beach['name']}, {lookup_result.province_name}",
            'lat': beach['lat'],
            'lon': beach['lon']
        }
        
        search_request = build_search_request(geo_data, filters)
        search_request['radius'] = search_data['radius_km'] * 1000
        
        # Search
        elements, search_error = search_accommodations(search_request)
        
        if search_error:
            st.warning(f"⚠️ {search_error}")
            st.session_state.search_step = 'input'
        elif not elements:
            st.info("😕 Không tìm thấy kết quả nào.")
            st.session_state.search_step = 'input'
        else:
            # Normalize & Filter & Rank
            accommodations = normalize_osm_data(elements)
            filtered = filter_results(accommodations, search_request)
            
            if not filtered:
                st.info("😕 Không có kết quả phù hợp với bộ lọc.")
                st.session_state.search_step = 'input'
            else:
                top_results = rank_results(filtered, search_request)
                st.session_state.search_results = top_results
                
                # Update search_data for Q&A
                st.session_state.search_data.update({
                    'beach_name': beach['name'],
                    'province_name': lookup_result.province_name,
                    'tags': filters.get('tags', [])
                })
                
                # Initialize Q&A handler
                st.session_state.qa_handler.initialize(
                    st.session_state.search_data,
                    top_results
                )
                
                # Save to Firebase
                firebase_service.save_search_history(
                    st.session_state.user_id,
                    {
                        'location': search_data['location'],
                        'beach': beach['name'],
                        'province': lookup_result.province_name,
                        'budget': filters['budget'],
                        'type': filters['type'],
                        'results_count': len(top_results),
                        'top_results': [
                            {
                                'name': r.get('name', 'N/A'),
                                'type': r.get('type', 'N/A'),
                                'score': r.get('score', 0)
                            }
                            for r in top_results[:3]
                        ]
                    }
                )
                
                st.session_state.search_step = 'results'
                st.rerun()

# ============================================================================
# STEP 4: RESULTS + Q&A
# ============================================================================

elif st.session_state.search_step == 'results':
    results = st.session_state.search_results
    search_data = st.session_state.search_data
    
    st.markdown(f"### 🎯 Top {len(results)} nơi ở tại {search_data.get('beach_name', '')}")
    
    # Display results
    for acc in results:
        name = acc.get('name', 'Unnamed')
        acc_type = acc.get('type', 'hotel')
        tags = acc.get('tags', [])
        score = acc.get('score', 0.0)
        distance = acc.get('distance', 0)
        rating = acc.get('rating', 0)
        reviews = acc.get('reviews', 0)
        location = acc.get('location', (0, 0))
        rank = acc.get('rank', '?')
        price_level = acc.get('price_level', 'N/A')
        address = acc.get('address', '')
        
        distance_str = format_distance(distance) if distance else "N/A"
        
        latlon = ("N/A", "N/A")
        if isinstance(location, (list, tuple)) and len(location) >= 2:
            latlon = (f"{location[0]:.5f}", f"{location[1]:.5f}")
        
        # Rating display
        rating_stars = "⭐" * int(rating) if rating else ""
        
        card_html = f"""
        <div class='result-card'>
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;'>
                <div>
                    <span class='rank-badge'>#{rank}</span>
                    <strong style='font-size:1.2rem; margin-left:8px;'>{name}</strong>
                </div>
                <div>
                    <span class='score-badge'>🏆 {score:.1f}</span>
                    <span class='distance-badge'>📍 {distance_str}</span>
                </div>
            </div>
            <div style='color:#555; margin-bottom:8px;'>
                <strong>Loại:</strong> {acc_type} | 
                <strong>Giá:</strong> {price_level} |
                <strong>Rating:</strong> {rating}/5 {rating_stars} ({reviews} đánh giá)
            </div>
            <div style='color:#666; margin-bottom:8px;'>
                <strong>Tags:</strong> {', '.join(tags[:5]) if tags else 'N/A'}
            </div>
            <div style='font-size:0.85rem; color:#888;'>
                📍 {address if address else f'Lat: {latlon[0]}, Lon: {latlon[1]}'}
                <a href="https://www.google.com/maps/search/?api=1&query={latlon[0]},{latlon[1]}" target="_blank" style="margin-left:10px;">
                    🗺️ Xem bản đồ
                </a>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    
    # ============================================================================
    # Q&A SECTION
    # ============================================================================
    
    st.markdown("---")
    st.markdown("### 💬 Hỏi đáp về kết quả")
    
    # Suggested questions
    st.markdown("**📝 Câu hỏi gợi ý:**")
    suggested_cols = st.columns(3)
    suggested_questions = get_allowed_questions_display()
    
    for i, q in enumerate(suggested_questions):
        with suggested_cols[i % 3]:
            if st.button(q, key=f"suggest_{i}", use_container_width=True):
                # Process question
                answer, is_valid = st.session_state.qa_handler.process_question(q)
                st.session_state.chat_messages.append({
                    'role': 'user',
                    'content': q
                })
                st.session_state.chat_messages.append({
                    'role': 'assistant',
                    'content': answer
                })
                st.rerun()
    
    # Chat history
    if st.session_state.chat_messages:
        st.markdown("---")
        for msg in st.session_state.chat_messages:
            if msg['role'] == 'user':
                st.markdown(f"**🧑 Bạn:** {msg['content']}")
            else:
                st.markdown(f"**🤖 Bot:** {msg['content']}")
        st.markdown("---")
    
    # Custom question input
    with st.form("qa_form", clear_on_submit=True):
        user_question = st.text_input(
            "Hoặc nhập câu hỏi của bạn:",
            placeholder="Tại sao lại đề xuất nơi này?"
        )
        ask_btn = st.form_submit_button("Gửi", use_container_width=True)
    
    if ask_btn and user_question:
        answer, is_valid = st.session_state.qa_handler.process_question(user_question)
        st.session_state.chat_messages.append({
            'role': 'user',
            'content': user_question
        })
        st.session_state.chat_messages.append({
            'role': 'assistant',
            'content': answer
        })
        st.rerun()
    
    # Reset button
    st.markdown("---")
    if st.button("🔄 Tìm kiếm mới", use_container_width=True):
        reset_search()
        st.rerun()