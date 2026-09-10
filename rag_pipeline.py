"""
Milestone 2: Financial Document RAG Pipeline
Loads a financial PDF, splits it carefully, creates embeddings, and stores in ChromaDB.
"""

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Configuration
DATA_FOLDER = "data"
CHROMA_PERSIST_DIR = "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVER_K = 3


class FinancialDocumentRAG:
    """RAG pipeline for financial documents."""
    
    def __init__(self, pdf_path: str, persist_directory: str = CHROMA_PERSIST_DIR):
        """
        Initialize the RAG pipeline.
        
        Args:
            pdf_path: Path to the financial PDF document
            persist_directory: Directory to persist ChromaDB
        """
        self.pdf_path = pdf_path
        self.persist_directory = persist_directory
        self.documents = []
        self.chunks = []
        self.vectorstore = None
        self.retriever = None
        
    def load_document(self):
        """Load the financial PDF document."""
        print(f"Loading document: {self.pdf_path}")
        loader = PyPDFLoader(self.pdf_path)
        self.documents = loader.load()
        print(f"✓ Loaded {len(self.documents)} pages")
        return self.documents
    
    def split_document(self):
        """
        Split document into chunks carefully to preserve financial data context.
        Uses RecursiveCharacterTextSplitter with moderate chunk size and overlap
        to avoid separating numbers from their labels.
        """
        print(f"\nSplitting document with chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP}")
        
        # Use RecursiveCharacterTextSplitter which is better at keeping
        # related content together (like tables and financial figures)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],  # Prioritize paragraph breaks
        )
        
        self.chunks = text_splitter.split_documents(self.documents)
        print(f"✓ Created {len(self.chunks)} chunks")
        
        # Show sample chunk for verification
        if self.chunks:
            print(f"\nSample chunk (first 300 chars):")
            print("-" * 60)
            print(self.chunks[0].page_content[:300] + "...")
            print("-" * 60)
        
        return self.chunks
    
    def create_vectorstore(self):
        """Create embeddings and store in ChromaDB with persistence."""
        print(f"\nInitializing HuggingFace embeddings: {EMBEDDING_MODEL}")
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},  # Use CPU for compatibility
            encode_kwargs={'normalize_embeddings': True}
        )
        
        print(f"Creating ChromaDB vector store (persist to: {self.persist_directory})")
        
        # Check if vector store already exists
        if os.path.exists(self.persist_directory):
            print("⚠ Existing ChromaDB found. Loading from disk...")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=embeddings
            )
            print(f"✓ Loaded existing vector store")
        else:
            print(f"Creating new ChromaDB vector store (this may take a few minutes for {len(self.chunks)} chunks)...")
            self.vectorstore = Chroma.from_documents(
                documents=self.chunks,
                embedding=embeddings,
                persist_directory=self.persist_directory
            )
            print(f"✓ Created and persisted vector store")
        
        return self.vectorstore
    
    def create_retriever(self):
        """Create a retriever with k=3."""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Call create_vectorstore() first.")
        
        print(f"\nCreating retriever with k={RETRIEVER_K}")
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": RETRIEVER_K}
        )
        print(f"✓ Retriever configured")
        return self.retriever
    
    def test_retrieval(self, query: str):
        """
        Test retrieval for a given query.
        
        Args:
            query: Question to search for
            
        Returns:
            List of retrieved documents
        """
        if not self.retriever:
            raise ValueError("Retriever not initialized. Call create_retriever() first.")
        
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print('='*60)
        
        results = self.retriever.invoke(query)
        
        print(f"Retrieved {len(results)} chunks:\n")
        for i, doc in enumerate(results, 1):
            print(f"[Chunk {i}]")
            print(f"Source: Page {doc.metadata.get('page', 'N/A')}")
            print(f"Content preview (first 400 chars):")
            print("-" * 60)
            print(doc.page_content[:400])
            if len(doc.page_content) > 400:
                print("...")
            print("-" * 60)
            print()
        
        return results
    
    def build_pipeline(self):
        """Build the complete RAG pipeline."""
        print("=" * 60)
        print("Building Financial Document RAG Pipeline")
        print("=" * 60)
        
        # Step 1: Load document
        self.load_document()
        
        # Step 2: Split document
        self.split_document()
        
        # Step 3: Create vector store
        self.create_vectorstore()
        
        # Step 4: Create retriever
        self.create_retriever()
        
        print("\n" + "=" * 60)
        print("✓ RAG Pipeline Built Successfully")
        print("=" * 60)
        
        return self


def main():
    """Main function to build and test the RAG pipeline."""
    
    # Find the PDF file in data folder
    pdf_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("❌ No PDF files found in data/ folder")
        return
    
    pdf_path = os.path.join(DATA_FOLDER, pdf_files[0])
    print(f"Using document: {pdf_path}\n")
    
    # Build RAG pipeline
    rag = FinancialDocumentRAG(pdf_path)
    rag.build_pipeline()
    
    # Test queries
    print("\n" + "=" * 60)
    print("TESTING RETRIEVAL")
    print("=" * 60)
    
    test_queries = [
        "What was the company's revenue?",
        "What was the company's net income?",
        "What was the company's operating cash flow?"
    ]
    
    for query in test_queries:
        rag.test_retrieval(query)
    
    # Summary
    print("\n" + "=" * 60)
    print("MILESTONE 2 SUMMARY")
    print("=" * 60)
    print(f"A. Document Loading: ✓ SUCCESS ({len(rag.documents)} pages)")
    print(f"B. Chunks Created: {len(rag.chunks)}")
    print(f"C. Chroma Persistence: ✓ {rag.persist_directory}")
    print(f"D. Retriever Config: k={RETRIEVER_K}")
    print(f"E. Test Queries: {len(test_queries)} executed")
    print("=" * 60)


if __name__ == "__main__":
    main()
