"""
Hero Section Component
"""

import streamlit as st


def render_hero():
    """Render hero section với title và subtitle"""
    st.markdown("""
    <div class='hero-title'>Beach Accommodation Finder</div>
    <div class='hero-subtitle'>Tìm kiếm nơi ở gần bãi biển bằng AI thông minh</div>
    """, unsafe_allow_html=True)