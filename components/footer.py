"""
Footer Component
"""

import streamlit as st


def render_footer():
    """Render footer"""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 1rem 0;'>
        <p>Đồ án Tư duy Tính toán - Năm 2 | Trananhkhoa2929 | 2025</p>
        <p style='font-size: 0.85rem;'>Powered by 🤖 Gemini AI + 🗺️ OpenStreetMap + 🔥 Firebase + 🎨 Streamlit</p>
    </div>
    """, unsafe_allow_html=True)