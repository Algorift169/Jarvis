import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Groq API key (free from console.groq.com)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# OpenAI API key (optional, for fallback)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Wake word
WAKE_WORD = "jarvis"

# Voice settings
VOICE_RATE = 160
VOICE_VOLUME = 1.0

# Speech recognition settings
MIC_INDEX = 0
RECOGNITION_TIMEOUT = 5

# Conversation settings
CONVERSATION_TIMEOUT = 60