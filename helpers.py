import logging
from langdetect import detect
from config import COMPANY_NAME, COMPANY_LOCATION, COMPANY_EMAIL, COMPANY_PHONE
import os

# Define a list of gratitude words
gratitude_words = ['thank', 'grazie', 'merci', 'gracias']

def detect_language(text):
    """Detect the language of user input with a focus on common greetings."""
    try:
        # Clean the text
        cleaned_text = text.strip().lower()
        
        # Explicitly handle common greetings for short texts
        if len(cleaned_text) <= 20:
            english_greetings = ['hi', 'hello', 'good morning', 'good evening', 'thanks', 'thank you']
            italian_greetings = ['ciao', 'buongiorno', 'buonasera', 'grazie', 'prego']
            french_greetings = ['bonjour', 'salut', 'merci']
            spanish_greetings = ['hola', 'buenos días', 'gracias']
            
            if cleaned_text in english_greetings:
                return 'en'
            elif cleaned_text in italian_greetings:
                return 'it'
            elif cleaned_text in french_greetings:
                return 'fr'
            elif cleaned_text in spanish_greetings:
                return 'es'
        
        # Use langdetect for longer texts
        detected_lang = detect(cleaned_text)
        logging.debug(f"Detected language via langdetect: {detected_lang}")
        
        return detected_lang
        
    except Exception as e:
        logging.error(f"Language detection error: {e}")
        return 'it'  # Default to Italian on error

def validate_input(text):
    """Validate user input"""
    if not text or not text.strip():
        return False, "Please provide a message."
    
    if len(text.strip()) > 1000:
        return False, "Message too long. Please keep it under 1000 characters."
    
    return True, ""

def format_response(text):
    """Format the response text"""
    # Remove extra whitespace
    formatted = text.strip()
    
    # Ensure proper sentence ending
    if formatted and not formatted.endswith(('.', '!', '?')):
        formatted += '.'
    
    return formatted

def ensure_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        "data/vector_store",
        "data/pdfs",
        "data/text_files",
        "static",
        "images"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("All directories ensured")

def handle_user_message(user_message):
    """Process the user message and generate a response."""
    # Detect language
    detected_language = detect_language(user_message)
    logging.debug(f"Detected language: {detected_language}")
    
    # Check for casual greeting
    if is_casual_greeting(user_message):
        logging.debug("Casual greeting detected.")
        # Handle casual greeting directly
        if any(word in user_message.lower() for word in gratitude_words):
            response = get_gratitude_response(detected_language)
            logging.debug(f"Generated gratitude response: {response}")
            return response
        else:
            response = get_casual_greeting_response(detected_language)
            logging.debug(f"Generated casual greeting response: {response}")
            return response
    
    # If not a casual greeting, proceed with normal processing
    logging.debug("Proceeding with normal processing.")
    prompt = get_system_prompt(detected_language, user_message)
    return query_language_model(prompt)

def is_casual_greeting(text):
    """Check if the message is a casual greeting or simple expression"""
    # List of casual greetings and expressions
    casual_phrases = [
        'ciao', 'hello', 'hi', 'bonjour', 'salut', 'hola', 'buongiorno', 'good morning',
        'thank you', 'thanks', 'grazie', 'merci', 'gracias', 'bye', 'goodbye', 'arrivederci',
        'see you', 'take care', 'buenos días', 'hey there', 'hi, how are you?'
    ]
    
    # Normalize the text to lowercase
    normalized_text = text.lower().strip()
    
    # Check if the entire text matches any of the casual phrases
    result = normalized_text in casual_phrases
    logging.debug(f"Checking if '{text}' is a casual greeting: {result}")
    return result

def get_gratitude_response(language_code):
    """Return a predefined gratitude response."""
    gratitude_responses = {
        'it': "Prego! 😊 C'è qualcos'altro con cui posso aiutarti?",
        'en': "You're welcome! 😊 Is there anything else I can do for you?",
        'fr': "Je vous en prie ! 😊 Y a-t-il autre chose que je peux faire pour vous ?",
        'es': "¡De nada! 😊 ¿Hay algo más en lo que pueda ayudarte?"
    }
    return gratitude_responses.get(language_code, gratitude_responses['en'])

def get_casual_greeting_response(language_code):
    """Return a predefined casual greeting response."""
    casual_responses = {
        'it': f"Ciao! Sono Benedetta da {COMPANY_NAME}. Come posso aiutarti oggi?",
        'en': f"Hello! I'm Benedetta from {COMPANY_NAME}. How can I help you today?",
        'fr': f"Bonjour! Je suis Benedetta de {COMPANY_NAME}. Comment puis-je vous aider aujourd'hui?",
        'es': f"¡Hola! Soy Benedetta de {COMPANY_NAME}. ¿Cómo puedo ayudarte hoy?"
    }
    return casual_responses.get(language_code, casual_responses['en'])

def get_system_prompt(language_code, user_message):
    """Get appropriate prompt based on message type"""
    
    # Clear prompt that instructs to use context
    prompt = f"""You are Benedetta, virtual assistant for {COMPANY_NAME} in Crotone, Italy. 
Use any provided context to answer accurately. 
Company: {COMPANY_NAME}, Location: {COMPANY_LOCATION}, Email: {COMPANY_EMAIL}, Phone: {COMPANY_PHONE}
Respond in the same language as the question: {user_message}"""
    
    logging.debug(f"Generated universal prompt: {prompt}")
    return prompt

def query_language_model(prompt):
    """Query the language model with the given prompt."""
    # Your existing logic to query the language model
    pass
