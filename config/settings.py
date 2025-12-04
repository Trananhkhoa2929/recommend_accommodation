"""
Application Settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ===========================================
# API KEYS
# ===========================================
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
FIREBASE_DATABASE_URL = os.getenv('FIREBASE_DATABASE_URL')

# ===========================================
# APP CONFIG
# ===========================================
APP_NAME = "Beach Accommodation Finder"
APP_ICON = "🏖️"
APP_VERSION = "2.0.0"

# ===========================================
# SEARCH CONFIG
# ===========================================
DEFAULT_SEARCH_RADIUS = 5000  # meters
MAX_RESULTS = 10
TOP_RESULTS_COUNT = 5

# ===========================================
# PAGE CONFIG
# ===========================================
PAGE_CONFIG = {
    "page_title": APP_NAME,
    "page_icon": APP_ICON,
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}