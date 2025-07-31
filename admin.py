from rag import FurnitureRAG

# Initialize the RAG system
rag = FurnitureRAG()

while True:
    print("\nOptions:")
    print("1. Add PDF document")
    print("2. Add text document")  # ✅ NEW: Add text file support!
    print("3. Add website content")
    print("4. Process all documents")
    print("5. Test a query")
    print("6. Exit")
    
    choice = input("\nEnter your choice (1-6): ")
    
    if choice == '1':
        pdf_path = input("Enter the path to the PDF file: ")
        rag.add_pdf(pdf_path)
        print(f"Added PDF: {pdf_path}")

    elif choice == '2': 
        text_path = input("Enter the path to the text file: ")
        rag.add_text(text_path)  
        print(f"Added text file: {text_path}")

    elif choice == '3':
        url = input("Enter the website URL: ")
        rag.add_website(url)
        print(f"Added website: {url}")

    elif choice == '4':
        print("Processing documents...")
        rag.process_documents()
        print("Documents processed and vector store created.")

    elif choice == '5':
        query = input("Enter a test query: ")
        print("\nGenerating response...")
        response = rag.query(query)
        print("\nResponse:")
        print(response)

    elif choice == '6':
        print("Exiting...")
        break
    
    else:
        print("Invalid choice. Please try again.")