import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"

BASE_DIR = os.getcwd()

UPLOAD_DIR = os.path.join(BASE_DIR, "storage", "uploads")
CHAT_DIR = os.path.join(BASE_DIR, "storage", "chats")
DB_DIR = os.path.join(BASE_DIR, "storage", "chroma_db")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHAT_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Please add it inside your .env file.")