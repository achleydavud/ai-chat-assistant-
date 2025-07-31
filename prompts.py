import logging
from helpers import (
    detect_language,
    is_casual_greeting,
    get_gratitude_response,
    get_casual_greeting_response,
    get_system_prompt,
    query_language_model
)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def handle_user_message(user_message):
    """Process the user message and generate a response."""
    logging.debug(f"Received user message: {user_message}")
    
    # Detect language using the function from helpers.py
    language_code = detect_language(user_message)
    logging.debug(f"Detected language: {language_code}")
    
    # Check for casual greeting
    if is_casual_greeting(user_message):
        logging.debug("Casual greeting detected.")
        # Handle casual greeting directly
        if any(word in user_message.lower() for word in ['thank', 'grazie', 'merci', 'gracias']):
            response = get_gratitude_response(language_code)
            logging.debug(f"Generated gratitude response: {response}")
            return response
        else:
            response = get_casual_greeting_response(language_code)
            logging.debug(f"Generated casual greeting response: {response}")
            return response
    
    # If not a casual greeting, proceed with normal processing
    logging.debug("Proceeding with normal processing.")
    prompt = get_system_prompt(language_code, user_message)
    logging.debug(f"Generated prompt: {prompt}")
    response = query_language_model(prompt)
    logging.debug(f"Model response: {response}")
    return response
