"""
Beach Accommodation Finder - Main Entry Point
Đồ án Tư duy Tính toán - Năm 2
"""

import streamlit as st
import uuid
import sys
from pathlib import Path

# Thêm thư mục gốc vào sys.path để import được các module
ROOT_DIR = Path(__file__). parent
sys.path.insert(0, str(ROOT_DIR))

# Config
from config.settings import PAGE_CONFIG
from config.styles import CUSTOM_CSS

# Components
from components import (
    render_sidebar,
    render_hero,
    render_chat_bot,
    render_features,
    render_stats,
    render_footer
)

# ============================================================================
# PAGE SETUP
# ============================================================================

st. set_page_config(**PAGE_CONFIG)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]

# ============================================================================
# RENDER PAGE
# ============================================================================

# Sidebar
render_sidebar(st. session_state. user_id)

# Hero Section
render_hero()

# Chat Bot (USP)
render_chat_bot()

# Features
render_features()

# Stats
render_stats()

# CTA
st.markdown("---")
st. info("👈 **Chọn trang từ menu bên trái để bắt đầu! **")

# Footer
render_footer()