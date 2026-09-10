"""
Test script for the Investment Research Agent
Demonstrates the agent's capabilities with various types of questions.
"""

from agent.investment_agent import create_investment_agent


def test_agent():
    """Test the investment research agent with sample queries."""
    
    print("=" * 70)
    print("InvestIQ - Investment Research Agent Test")
    print("=" * 70)
    print("\n🤖 Initializing agent with Qwen 2.5 7B...")
    
    try:
        # Create agent
        agent = create_investment_agent(model_name="qwen2.5:7b")
        print("✓ Agent initialized successfully\n")
        
        # Test queries
        test_queries = [
            {
                "category": "Live Stock Price",
                "query": "What is Apple's current stock price?",
                "description": "Tests live market data tool"
            },
            {
                "category": "Financial Document",
                "query": "What was Apple's revenue according to the 10-K?",
                "description": "Tests RAG document retrieval"
            },
            {
                "category": "Company Fundamentals",
                "query": "What are Apple's key financial metrics and fundamentals?",
                "description": "Tests company fundamentals tool"
            },
            {
                "category": "Investment Analysis",
                "query": "Should I invest in Apple? Give me a comprehensive analysis.",
                "description": "Tests multi-tool usage and analysis"
            }
        ]
        
        print("=" * 70)
        print("RUNNING TEST QUERIES")
        print("=" * 70)
        
        for i, test in enumerate(test_queries, 1):
            print(f"\n{'=' * 70}")
            print(f"Test {i}/{len(test_queries)}: {test['category']}")
            print(f"{'=' * 70}")
            print(f"\n📝 Query: {test['query']}")
            print(f"🎯 Purpose: {test['description']}")
            print(f"\n🤖 Agent Response:")
            print("-" * 70)
            
            try:
                response = agent.run(test['query'])
                print(response)
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print("-" * 70)
            
            # Pause between queries to respect rate limits
            if i < len(test_queries):
                print("\n⏸️  Pausing for 15 seconds (API rate limit)...")
                import time
                time.sleep(15)
        
        print(f"\n{'=' * 70}")
        print("✅ All tests completed")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


def interactive_mode():
    """Run the agent in interactive mode."""
    
    print("=" * 70)
    print("InvestIQ - Investment Research Agent (Interactive Mode)")
    print("=" * 70)
    print("\n🤖 Initializing agent...")
    
    try:
        agent = create_investment_agent(model_name="qwen2.5:7b")
        print("✓ Agent initialized successfully")
        print("\n💡 Tips:")
        print("  - Ask about stock prices, company fundamentals, or financial documents")
        print("  - Type 'quit' or 'exit' to stop")
        print("  - Type 'examples' to see sample questions")
        print("\n" + "=" * 70)
        
        while True:
            try:
                user_input = input("\n🔍 Your question: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if user_input.lower() == 'examples':
                    print("\n📋 Example Questions:")
                    print("  1. What is Apple's current stock price?")
                    print("  2. What was the company's revenue according to the 10-K?")
                    print("  3. What are Microsoft's fundamentals?")
                    print("  4. How has Tesla performed historically?")
                    print("  5. What's the latest news about NVDA?")
                    print("  6. Analyze Amazon as an investment")
                    continue
                
                print("\n🤖 Agent thinking...\n")
                response = agent.run(user_input)
                print("\n" + "=" * 70)
                print("📊 Response:")
                print("=" * 70)
                print(response)
                print("=" * 70)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    except Exception as e:
        print(f"\n❌ Error initializing agent: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import sys
    
    print("\n" + "=" * 70)
    print("InvestIQ Test Options")
    print("=" * 70)
    print("\n1. Run automated tests (default)")
    print("2. Interactive mode")
    print("\nChoose an option (1 or 2), or press Enter for option 1:")
    
    choice = input("Your choice: ").strip()
    
    if choice == "2":
        interactive_mode()
    else:
        test_agent()
