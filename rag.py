import os
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

class FurnitureRAG:
    
    def __init__(self, model_name="llama3.2:latest"):
        self.model_name = model_name
        self.documents = []
        self.vector_store = None
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.llm = Ollama(model=model_name)
        
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        os.makedirs("data/pdfs", exist_ok=True)
        os.makedirs("data/vector_store", exist_ok=True)
        
    def add_pdf(self, pdf_path):
        """Add a PDF document to the knowledge base"""
        loader = PyPDFLoader(pdf_path)
        self.documents.extend(loader.load())
        print(f"Added PDF: {pdf_path}")
        return self
    
    def add_text(self, text_path):
        """Add a text document to the knowledge base"""
        loader = TextLoader(text_path, encoding="utf-8")  # Explicit encoding!
        self.documents.extend(loader.load())  
        print(f"Added TEXT: {text_path}")  
        return self

    
    def add_website(self, url):
        """Add content from a website to the knowledge base"""
        loader = WebBaseLoader(url)
        self.documents.extend(loader.load())
        print(f"Added website: {url}")
        return self
    
    def process_documents(self):
        """Process documents into chunks and create vector store"""
        if not self.documents:
            print("No documents to process")
            return self
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(self.documents)
        print(f"Storing {len(chunks)} documents in the vector store...")
        print(f"Split into {len(chunks)} chunks")
        
        # Create vector store
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        
        # Save the vector store
        self.vector_store.save_local("data/vector_store")
        print("Vector store created and saved")
        return self
    
    def load_vector_store(self):
        """Load an existing vector store"""
        if os.path.exists("data/vector_store"):
            self.vector_store = FAISS.load_local("data/vector_store", self.embeddings)
            print("Vector store loaded")
        else:
            print("No vector store found")
        return self
    
    def query(self, question, use_retrieval=True):
        """Query the system with or without retrieval"""
        if use_retrieval and self.vector_store:
            # Create a retrieval chain
            retriever = self.vector_store.as_retriever(
                search_kwargs={"k": 3}  # Return top 3 relevant chunks
            )
            
            # Get relevant documents
            docs = retriever.invoke(question)

            
            # Create context from retrieved documents
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Create prompt with context
            prompt = f"""You are a helpful assistant for a furniture company.
            Use the following information to answer the question.
            
            Context:
            {context}
            
            Question: {question}
            
            Answer:"""
            
            # Query Ollama directly
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt
                }
            )
            
            # Process streaming response
            full_response = ""
            for line in response.iter_lines():
                if line:
                    line_json = line.decode('utf-8')
                    import json
                    result = json.loads(line_json)
                    if 'response' in result:
                        full_response += result['response']
            
            return full_response
        else:
            # Direct query without retrieval
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": f"Question: {question}\nAnswer:"
                }
            )
            
            # Process streaming response
            full_response = ""
            for line in response.iter_lines():
                if line:
                    line_json = line.decode('utf-8')
                    import json
                    result = json.loads(line_json)
                    if 'response' in result:
                        full_response += result['response']
            
            return full_response
