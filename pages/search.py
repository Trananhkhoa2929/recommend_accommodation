# (chỉ phần hiển thị results — thay thế đoạn loop hiện results của bạn bằng code bên dưới)
# Giả sử bạn đã có `ranked` list từ pipeline

import streamlit as st
from src.utils.formatters import format_distance
from src.backend.ranking import top_results

st.markdown("---")
st.markdown(f"### 🎯 Top {len(top_results)} nơi ở được đề xuất")

for acc in top_results:
    # Defensive: lấy giá trị an toàn
    name = acc.get('name', 'Unnamed')
    acc_type = acc.get('type', 'accommodation')
    tags = acc.get('tags', [])
    score = acc.get('score', 0.0)
    distance = acc.get('distance', None)
    location = acc.get('location', None)

    # Format distance an toàn
    try:
        distance_str = format_distance(distance) if distance is not None else "N/A"
    except Exception:
        distance_str = "N/A"

    # Lat/Lon an toàn
    latlon = ("N/A", "N/A")
    try:
        if isinstance(location, (list, tuple)) and len(location) >= 2:
            latlon = (f"{float(location[0]):.5f}", f"{float(location[1]):.5f}")
    except Exception:
        latlon = ("N/A", "N/A")

    # Render bằng HTML nhỏ (unsafe_allow_html True) hoặc components.html
    card_html = f"""
    <div style='background:#fff; border-radius:12px; padding:12px; margin-bottom:12px; box-shadow:0 6px 20px rgba(0,0,0,0.06);'>
      <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
        <div style='font-weight:700;'>#{acc.get('rank', '?')} - {name}</div>
        <div style='display:flex; gap:8px; align-items:center;'>
          <div style='background:#4caf50; color:#fff; padding:6px 8px; border-radius:8px;'>⭐ {score:.1f}</div>
          <div style='background:#2196f3; color:#fff; padding:6px 8px; border-radius:8px;'>📍 {distance_str}</div>
        </div>
      </div>
      <div style='color:#444; margin-bottom:6px;'>
        <strong>Loại:</strong> {acc_type} &nbsp;|&nbsp; <strong>Tags:</strong> {', '.join(tags[:5])}
      </div>
      <div style='font-size:0.9rem; color:#666;'>
        <a href="https://www.google.com/maps/search/?api=1&query={latlon[0]},{latlon[1]}" target="_blank">📍 Xem trên Google Maps</a>
        &nbsp;&nbsp; <span>Lat: {latlon[0]}, Lon: {latlon[1]}</span>
      </div>
    </div>
    """

    # Use st.markdown with unsafe_allow_html or components.html
    st.markdown(card_html, unsafe_allow_html=True)