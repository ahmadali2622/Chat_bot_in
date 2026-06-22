"""
config.py
---------
App configuration: environment variables, CORS settings, model config.
"""

import os
from dotenv import load_dotenv

# Load variables from .env file (if present)
load_dotenv()

# GROQ API Key (set this in your .env file)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Model name
GROQ_MODEL = "llama-3.1-8b-instant"

# CORS settings — restrict allowed_origins in production
ALLOWED_ORIGINS = ["*"]
