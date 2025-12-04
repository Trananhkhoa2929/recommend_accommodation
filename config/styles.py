"""
Custom CSS Styles
"""

CUSTOM_CSS = """
<style>
    /* ========== GLASS CARD ========== */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* ========== CHAT STYLES ========== */
    .chat-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        max-height: 600px;
        overflow-y: auto;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    . chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin: 0.8rem 0;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
        border-left: 4px solid #00bcd4;
        margin-right: 10%;
    }
    
    /* ========== USP ITEMS ========== */
    .usp-item {
        display: flex;
        align-items: flex-start;
        padding: 0.8rem 0;
        border-bottom: 1px solid #eee;
    }
    
    .usp-item:last-child {
        border-bottom: none;
    }
    
    .usp-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
        min-width: 40px;
    }
    
    /* ========== HERO ========== */
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* ========== FEATURE CARDS ========== */
    .feature-card {
        background: linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #e0e0e0;
        height: 100%;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.8rem;
    }
    
    /* ========== STATS ========== */
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 800;
    }
    
    .stat-label {
        font-size: 0.85rem;
        opacity: 0.9;
    }
    
    /* ========== COMPARE TABLE ========== */
    .compare-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
    }
    
    .compare-table th, .compare-table td {
        padding: 10px;
        text-align: center;
        border-bottom: 1px solid #eee;
    }
    
    .compare-table th {
        background: #f5f5f5;
        font-weight: 600;
    }
    
    /* ========== RESULT CARDS ========== */
    .result-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
    }
    
    .rank-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    .score-badge {
        background: #4caf50;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 10px;
        font-size: 0.85rem;
        margin-left: 0.5rem;
    }
    
    . distance-badge {
        background: #2196f3;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 10px;
        font-size: 0.85rem;
        margin-left: 0.5rem;
    }
    
    /* ========== HISTORY CARDS ========== */
    .history-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #11998e;
    }
    
    .history-date {
        color: #888;
        font-size: 0.85rem;
    }
    
    .history-location {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
        margin: 0.5rem 0;
    }
    
    .history-tag {
        background: #e8f5e9;
        color: #2e7d32;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
        display: inline-block;
        margin-bottom: 0.3rem;
    }
    
    /* ========== HEADERS ========== */
    .search-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .history-header {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    . about-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* ========== EMPTY STATE ========== */
    . empty-state {
        text-align: center;
        padding: 3rem;
        color: #888;
    }
    
    .empty-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    /* ========== PILLAR CARDS ========== */
    .pillar-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
    }
    
    .pillar-number {
        font-size: 1.8rem;
        font-weight: bold;
        opacity: 0.5;
    }
    
    /* ========== TECH CARDS ========== */
    .tech-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0. 1);
        height: 100%;
    }
    
    .tech-icon {
        font-size: 2.5rem;
        margin-bottom: 0.8rem;
    }
    
    /* ========== PROCESS STEPS ========== */
    .process-step {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
</style>
"""