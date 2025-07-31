# Model Configuration - EXTREME SPEED
OLLAMA_MODEL = "gemma3:1b"  # Much faster model
TEMPERATURE = 0.01  # Absolutely minimal for instant responses
NUM_PREDICT = 30  # Extremely short responses

# Rest stays the same...


# Server Configuration
HOST = "127.0.0.1"
PORT = 5000
DEBUG = True

# Company Information
COMPANY_NAME = "Schipani"
COMPANY_LOCATION = "Crotone, Italy"
COMPANY_EMAIL = "info@infissiearredamentikroton.it"
COMPANY_PHONE = "+39 0962 19 71 707"

# Paths
VECTOR_STORE_PATH = "data/vector_store"
TEXT_FILES_PATH = "data/text_files"
PDFS_PATH = "data/pdfs"

# Embeddings - faster model
EMBEDDINGS_MODEL = "all-MiniLM-L6-v2"  # Keep same for compatibility with existing vector store
