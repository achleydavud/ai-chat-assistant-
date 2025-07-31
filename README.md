# AI Chat Assistant 🤖 [WORK IN PROGRESS - NEEDS HELP!]

⚠️ **This project is currently buggy and needs contributors to help fix critical issues!**

A multilingual RAG-based chatbot for Schipani, an Italian furniture and door company. Built with Flask, Ollama, and FAISS vector store for intelligent customer support.

🚨 **CURRENT STATUS: PARTIALLY WORKING - MAJOR BUGS NEED FIXING**

## 🏢 About

AI Chat Assistant serves as a virtual customer service assistant can answer questions about:

- Company information and contact details
- Door catalogs and product specifications
- Product categories (SARA, VALENTINA, LINEA BUGNATA, LINEA ALVIN-SOFIA, etc.)
- Technical specifications and pricing

## ✨ Features (Partially Working)

- **🤖 RAG System**: Uses FAISS vector store with company knowledge base ⚠️ *Buggy with Italian*
- **🌍 Multilingual**: Supports Italian, English, French, and Spanish ⚠️ *Italian responses broken*
- **⚡ Fast Startup**: Lazy loading for quick application start ⚠️ *Buggy*
- **🎛️ Admin Panel**: System management and configuration interface ✅ *Works*
- **💬 Chat Interface**: Real-time conversation with message history ⚠️ *Very slow (30+ sec)*
- **🏗️ Modular Design**: Clean separation of concerns with Flask architecture ✅ *Works*

## 🚨 CRITICAL ISSUES THAT NEED FIXING

**This project currently has major bugs that make it unusable in production:**

1. **🔴 BROKEN: Italian queries return "I don't know"** despite having the information
2. **🔴 BROKEN: 30-40 second response times** (should be I think under 6-7 seconds)
3. **🔴 BROKEN: RAG system inconsistent** - sometimes works, sometimes doesn't
4. **🟡 Basic UI** - needs significant improvements

**We desperately need contributors to help fix these issues!**

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **LLM**: Ollama with Gemma3:1b model
- **Vector Store**: FAISS for document retrieval
- **Embeddings**: HuggingFace all-MiniLM-L6-v2
- **Frontend**: HTML, CSS, JavaScript
- **Knowledge Base**: Text files with company information

## 📋 Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- Gemma3:1b model downloaded (`ollama pull gemma3:1b`)

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd SchpaniAIassistent
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Ollama
```bash
# Install Ollama (if not already installed)
# Visit: https://ollama.ai/

# Pull the required model
ollama pull gemma3:1b

# Start Ollama service
ollama serve
```

### 5. Prepare Knowledge Base
Create the data directory structure:
```
data/
├── vector_store/      # Will be created automatically
├── text_files/        # Add your company knowledge files here
│   └── schipani_info.txt
└── pdfs/             # Optional: PDF documents
```

### 6. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
SchpaniAIassistent/
├── app.py                 # Main Flask application
├── helpers.py             # Utility functions and language detection
├── prompts.py             # Message handling and prompt management
├── config.py              # Configuration settings
├── rag.py                 # RAG system implementation
├── admin.py               # Admin panel functionality
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Chat interface
├── static/
│   ├── script.js         # Frontend JavaScript
│   ├── style.css         # Styling
│   └── images/
│       └── schpa.png     # Company logo
└── data/                 # Knowledge base (not in repo)
    ├── vector_store/     # FAISS vector database
    └── text_files/       # Company information files
```

## ⚙️ Configuration

Edit `config.py` to customize:

- **Model Settings**: Change Ollama model, temperature, token limits
- **Company Info**: Update company details and contact information
- **Server Settings**: Modify host, port, debug mode
- **Performance**: Adjust retrieval parameters and response settings

## 🐛 Known Issues & Bugs

We need your help to fix these issues:

### 🔴 High Priority
- **Italian Language Accuracy**: RAG responses in Italian are inconsistent
- **Response Time**: 20-30 second response times (too slow)
- **RAG Reliability**: Sometimes returns "I don't know" despite having information

### 🟡 Medium Priority
- **UI/UX Improvements**: Chat interface needs better styling and responsiveness
- **Error Handling**: Better error messages and fallback responses
- **Memory Management**: Optimize for lower memory usage

### 🟢 Low Priority
- **Additional Languages**: Expand language support
- **Advanced Admin Features**: More configuration options
- **API Documentation**: Add comprehensive API docs

## 🤝 How to Contribute

We welcome contributions! Here's how you can help:

### 🚀 Quick Start Contributing
1. **Fork** this repository
2. **Create** a feature branch (`git checkout -b fix-italian-responses`)
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

### 🎯 Areas Where We Need Help

#### 1. **LLM & RAG Optimization**
- Improve Italian language processing
- Optimize response times
- Better prompt engineering
- RAG retrieval accuracy

#### 2. **Frontend Development**
- Enhance chat UI/UX
- Mobile responsiveness
- Better error handling
- Loading indicators

#### 3. **Backend Improvements**
- Performance optimization
- Better error handling
- Code refactoring
- API improvements

#### 4. **Testing & Documentation**
- Unit tests
- Integration tests
- API documentation
- User guides

### 📋 Contribution Guidelines

1. **Issues First**: Check existing issues or create a new one
2. **Code Style**: Follow PEP 8 for Python code
3. **Testing**: Test your changes thoroughly
4. **Documentation**: Update docs if needed
5. **Small PRs**: Keep pull requests focused and small

### 🏷️ Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or improvement
- `help-wanted` - Extra attention is needed
- `good-first-issue` - Good for newcomers
- `performance` - Performance related
- `documentation` - Documentation improvements

## 📞 Contact & Support

- **Email**: achleydavud@gmail.com

## 🙏 Acknowledgments

- **Ollama Team** for the excellent LLM framework
- **HuggingFace** for embedding models
- **FAISS** for vector similarity search
- **Flask** community for the web framework

---

**⭐ If this project helps you, please give it a star!**

**🐛 Found a bug? Please create an issue!**

**💡 Have an idea? We'd love to hear it!**
