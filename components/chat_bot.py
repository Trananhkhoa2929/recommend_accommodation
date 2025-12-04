"""
Chat Bot Component - Hiển thị USP (Unique Selling Points)
Render bằng st.components.v1.html để đảm bảo HTML/CSS được thực thi (không hiện raw code)
"""
import streamlit as st
import streamlit.components.v1 as components

HTML = """
<div class='chat-container' style='font-family: "Inter", sans-serif;'>
  <!-- Welcome Message -->
  <div class='chat-message bot-message' style='padding:1rem; border-radius:10px;'>
    <strong>🤖 Beach Bot:</strong><br><br>
    Xin chào! Tôi là Beach Bot - trợ lý tìm kiếm nơi ở gần biển.
    <br><br>
    <strong>🤔 Tại sao bạn nên sử dụng Beach Finder thay vì các app khác?</strong><br><br>
    Để tôi giải thích nhé! 👇
  </div>

  <!-- USP Message -->
  <div class='chat-message bot-message' style='padding:1rem; margin-top:1rem;'>
    <strong>✨ Điểm khác biệt của chúng tôi:</strong><br><br>

    <div style='display:flex; gap:0.75rem; align-items:flex-start; margin-bottom:0.5rem;'>
      <div style='font-size:1.25rem;'>🤖</div>
      <div><strong>AI Hiểu Ngữ Cảnh</strong><br><small>Bạn gõ "vung tau" hay "Vũng Tàu" đều được — Gemini sẽ tự sửa.</small></div>
    </div>

    <div style='display:flex; gap:0.75rem; align-items:flex-start; margin-bottom:0.5rem;'>
      <div style='font-size:1.25rem;'>🗺️</div>
      <div><strong>Dữ Liệu Thực</strong><br><small>OpenStreetMap — dữ liệu mở, cập nhật.</small></div>
    </div>

    <div style='display:flex; gap:0.75rem; align-items:flex-start; margin-bottom:0.5rem;'>
      <div style='font-size:1.25rem;'>🏖️</div>
      <div><strong>Chuyên Biệt Cho Bãi Biển</strong><br><small>Tập trung cho các lựa chọn ven biển.</small></div>
    </div>
  </div>

  <!-- Compare Table -->
  <div class='chat-message bot-message' style='padding:1rem; margin-top:1rem;'>
    <strong>🆚 So sánh nhanh:</strong><br><br>
    <table style='width:100%; border-collapse:collapse; font-size:0.95rem;'>
      <tr style='background:#f5f5f5;'>
        <th style='padding:8px; text-align:left;'>Tính năng</th>
        <th style='padding:8px; text-align:center;'>Beach Finder</th>
        <th style='padding:8px; text-align:center;'>Booking/Agoda</th>
      </tr>
      <tr><td style='padding:8px;'>AI sửa lỗi chính tả</td><td style='text-align:center;'>✅</td><td style='text-align:center;'>❌</td></tr>
      <tr style='background:#fafafa;'><td style='padding:8px;'>Chuyên biệt ven biển</td><td style='text-align:center;'>✅</td><td style='text-align:center;'>❌</td></tr>
      <tr><td style='padding:8px;'>Dữ liệu OpenStreetMap</td><td style='text-align:center;'>✅</td><td style='text-align:center;'>❌</td></tr>
    </table>
  </div>

  <!-- CTA -->
  <div class='chat-message bot-message' style='padding:1rem; margin-top:1rem;'>
    <strong>🚀 Sẵn sàng bắt đầu?</strong><br><br>
    Chọn <strong>🔍 Search</strong> ở menu bên trái để tìm kiếm.
  </div>
</div>
"""

def render_chat_bot():
    """Render chat bot bằng một iframe HTML nhỏ để tránh Streamlit tự chặn/escape"""
    # Nếu bạn đã inject global CSS (config/styles.py), HTML ở trên vẫn dùng inline style để an toàn.
    # Sử dụng components.html để render raw HTML (với khả năng scroll)
    components.html(HTML, height=420, scrolling=True)