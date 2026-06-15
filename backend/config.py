"""
config.py
---------
App configuration: environment variables, CORS settings, model config.
"""

import os
from dotenv import load_dotenv

# Load variables from .env file (if present)
load_dotenv()

# Gemini API Key (set this in your .env file)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Model name
GEMINI_MODEL = "gemini-2.5-flash-lite"

# CORS settings — restrict allowed_origins in production
ALLOWED_ORIGINS = ["*"]
