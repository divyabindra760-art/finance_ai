"""
Milestone 1: Test ChatOllama connectivity
This script verifies that Ollama is running and accessible via LangChain.
"""

from langchain_ollama import ChatOllama

def test_ollama_connection():
    """Test basic connection to Ollama and get a simple response."""
    
    print("=" * 60)
    print("InvestIQ - Milestone 1: ChatOllama Connection Test")
    print("=" * 60)
    print()
    
    try:
        # Initialize ChatOllama with a common model
        # You can change the model name if you have a different one installed
        print("Initializing ChatOllama with model 'qwen3:0.6b'...")
        llm = ChatOllama(
            model="qwen3:0.6b",
            temperature=0.0,  # Deterministic for testing
        )
        print("✓ ChatOllama initialized successfully")
        print()
        
        # Test a simple invocation
        print("Sending test query: 'What is 2+2?'")
        response = llm.invoke("What is 2+2? Answer in one short sentence.")
        print()
        print("Response received:")
        print("-" * 60)
        print(response.content)
        print("-" * 60)
        print()
        
        print("✓ ChatOllama is working correctly!")
        print()
        print("Next steps:")
        print("1. Milestone 1 is complete")
        print("2. Ready to proceed to Milestone 2 (RAG pipeline)")
        
    except Exception as e:
        print("✗ Error connecting to Ollama:")
        print(f"  {type(e).__name__}: {e}")
        print()
        print("Troubleshooting:")
        print("1. Ensure Ollama is installed and running")
        print("2. Check that you have a model installed (e.g., 'ollama pull qwen3:0.6b')")
        print("3. Verify Ollama is accessible at http://localhost:11434")
        print("4. Try 'ollama list' to see available models")
        return False
    
    return True

if __name__ == "__main__":
    success = test_ollama_connection()
    exit(0 if success else 1)
