from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from langchain_community.llms import Ollama
from config import OLLAMA_MODEL, HOST, PORT, DEBUG
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from helpers import detect_language, validate_input, format_response, ensure_directories
from prompts import handle_user_message  # Use handle_user_message instead of get_system_prompt
import time
from prompts import handle_user_message, get_system_prompt



# Initialize Flask app
app = Flask(__name__)
CORS(app)

import time
startup_start = time.time()
print(f"=== STARTING APPLICATION ===")

# Ensure directories exist
print("Ensuring directories exist...")
step_start = time.time()
ensure_directories()
print(f"✓ Directories ready ({time.time() - step_start:.2f}s)")

# Use lazy loading for instant startup
print("Setting up lazy loading...")
step_start = time.time()

# Global variables for lazy loading
conversation_chain = None

def get_conversation_chain():
    global conversation_chain
    if conversation_chain is None:
        print("🔄 First request - loading AI components...")
        
        # Load embeddings and vector store
        print("Loading embeddings...")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        print("Loading vector store...")
        vector_store = FAISS.load_local("data/vector_store", embeddings, allow_dangerous_deserialization=True)
        print(f"Vector store loaded with documents")
        
        # Load language model
        print("Loading Ollama model...")
        llm = Ollama(
            model=OLLAMA_MODEL,
            temperature=0.05,
            num_predict=200,  # Enough for complete door listings
            top_k=3,
            top_p=0.7,
            repeat_penalty=1.2
        )
        print("Ollama model loaded")
        
        # Create conversation chain
        print("Creating conversation chain with RAG...")
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(search_kwargs={"k": 5}),  # Get more docs for complete listings
            return_source_documents=True
        )
        print("✅ RAG conversation chain ready!")
    else:
        print("Using existing conversation chain")
    
    return conversation_chain

print(f"✓ Lazy loading ready ({time.time() - step_start:.2f}s)")

# Initialize chat history
chat_history = []

# Skip warmup to reduce startup time (first query will be slightly slower)
print("Skipping warmup for faster startup...")

total_startup = time.time() - startup_start
print(f"=== APPLICATION READY IN {total_startup:.2f} SECONDS ===")
print(f"Server starting on http://{HOST}:{PORT}")
print(f"Open your browser and navigate to http://localhost:{PORT}")
print("="*50)

@app.before_request
def log_request_info():
    print(f"=== REQUEST: {request.method} {request.path} ===")
    if request.method == 'POST':
        print(f"Request data: {request.get_data()}")
        print(f"Content-Type: {request.content_type}")

@app.after_request
def log_response_info(response):
    print(f"=== RESPONSE: {response.status_code} ===")
    return response

@app.route('/')
def index():
    return render_template('index.html')

# BOTH routes for compatibility
@app.route('/chat', methods=['POST'])
@app.route('/api/chat', methods=['POST'])
def chat():
    start_time = time.time()
    print(f" Chat request started at: {time.strftime('%H:%M:%S')}")
    print("=== CHAT FUNCTION CALLED ===")

    try:
        print(f" Step 1 - Getting user message: {time.time() - start_time:.2f}s")
        global chat_history
        user_message = request.json.get('message', '')
        print(f"2. User message received: '{user_message}'")

        print(f" Step 2 - Input validation: {time.time() - start_time:.2f}s")
        # Validate input
        is_valid, error_message = validate_input(user_message)
        if not is_valid:
            return jsonify({"response": error_message})

        print(f" Step 3 - Language detection: {time.time() - start_time:.2f}s")
        # Detect language
        detected_language = detect_language(user_message)
        print(f"3. Detected language: {detected_language} for message: '{user_message}'")

        # Directly handle casual greetings
        response = handle_user_message(user_message)
        if response:
            print(f"Casual greeting or gratitude response: {response}")
            return jsonify({"response": response})

        print(f" Step 4 - Using RAG for all queries: {time.time() - start_time:.2f}s")
        
        # ALL queries use RAG system - that's where the knowledge is
        print("5. Using RAG system for all queries")
        
        # Check if this is specifically about products to customize the prompt
        product_keywords = ['door', 'doors', 'porte', 'porta', 'catalog', 'catalogo', 'product', 'prodotti', 'products', 'models', 'modelli', 'list', 'lista', 'show', 'mostra', 'hai', 'have', 'available', 'disponibili', 'cosa', 'what', 'quali', 'which', 'mobili', 'furniture', 'arredamenti', 'vendete', 'sell', 'offrite', 'offer']
        is_product_query = any(keyword in user_message.lower() for keyword in product_keywords)
        
        # Create appropriate question based on type - use English for better model understanding
        if is_product_query:
            enhanced_question = f"You are Benedetta from Schipani. List all doors from the context. Include names, codes, finishes. User asked: {user_message}"
        else:
            enhanced_question = f"You are Benedetta from Schipani company. Answer using the provided context about company info, location, contact details. User asked: {user_message}"
        
        print(f"Query type: {'Product' if is_product_query else 'General'}")
        print(f"Enhanced question: {enhanced_question}")
        print(f" Step 5 - Starting RAG query...")
        llm_start = time.time()
        
        response = get_conversation_chain()({
            "question": enhanced_question,
            "chat_history": chat_history
        })

        llm_end = time.time()
        print(f" Step 6 - LLM response received: {llm_end - llm_start:.2f}s (LLM only)")

        # DEBUG: Check retrieved documents
        if "source_documents" in response:
            print(f"7. Retrieved {len(response['source_documents'])} documents:")
            for i, doc in enumerate(response['source_documents']):
                print(f"   Doc {i+1}: {doc.page_content[:200]}...")
        else:
            print("7. WARNING: No source documents found in response!")
            print(f"   Response keys: {response.keys()}")

        answer = response["answer"]
        print(f"8. Raw answer: {answer}")

        print(f" Step 7 - Response formatting: {time.time() - start_time:.2f}s")
        # Format response
        formatted_answer = format_response(answer)
        print(f"9. Final response: {formatted_answer}")

        # Update chat history
        chat_history.append((user_message, formatted_answer))

        total_time = time.time() - start_time
        print(f" TOTAL TIME: {total_time:.2f}s")
        print(f" LLM took: {(llm_end - llm_start)/total_time*100:.1f}% of total time")

        return jsonify({
            "response": formatted_answer,
            "processing_time": f"{total_time:.2f}s"
        })

    except Exception as e:
        error_time = time.time() - start_time
        print(f" Error after {error_time:.2f}s: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
