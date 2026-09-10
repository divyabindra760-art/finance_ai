"""
InvestIQ - Gradio UI
AI-Powered Investment Research Assistant
"""

import os
import sys
import gradio as gr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.investment_agent import create_investment_agent


# Global agent instance
agent = None


def initialize_agent():
    """Initialize the investment research agent."""
    global agent
    try:
        agent = create_investment_agent(model_name="qwen3:0.6b")
        return True, "Agent initialized successfully"
    except Exception as e:
        return False, f"Error initializing agent: {str(e)}"


def chat_with_agent(message, history):
    """
    Process user message and return agent response.
    
    Args:
        message: User's question
        history: Chat history (list of message dicts with 'role' and 'content')
    
    Returns:
        Updated history with new exchange in Gradio 6.0 format
    """
    if not message or not message.strip():
        return history
    
    # Check if agent is initialized
    if agent is None:
        success, error_msg = initialize_agent()
        if not success:
            # Add user message
            history.append({"role": "user", "content": message})
            # Add error response
            history.append({
                "role": "assistant",
                "content": f"❌ **Error**: {error_msg}\n\nPlease ensure:\n- Ollama is running\n- Model qwen3:0.6b is installed\n- ChromaDB exists from Milestone 2"
            })
            return history
    
    try:
        # Add user message to history
        history.append({"role": "user", "content": message})
        
        # Get response from agent
        response = agent.run(message)
        
        # Add assistant response to history
        history.append({"role": "assistant", "content": response})
        
    except Exception as e:
        error_response = f"❌ **Error**: {str(e)}\n\nPlease check:\n- Ollama is running\n- Alpha Vantage API key is set in .env\n- ChromaDB is accessible"
        history.append({"role": "assistant", "content": error_response})
    
    return history


def clear_chat():
    """Clear the chat history."""
    return []


# Create Gradio interface
def create_ui():
    """Create the Gradio UI for InvestIQ."""
    
    # Custom CSS for better styling
    custom_css = """
    .disclaimer {
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        font-size: 14px;
    }
    .disclaimer-title {
        font-weight: bold;
        color: #856404;
        margin-bottom: 8px;
    }
    .disclaimer-text {
        color: #856404;
    }
    """
    
    with gr.Blocks(
        theme=gr.themes.Soft(),
        css=custom_css,
        title="InvestIQ - Investment Research Assistant"
    ) as demo:
        
        # Header
        gr.Markdown(
            """
            # 🔎 InvestIQ
            ### AI-Powered Investment Research Assistant
            
            Ask questions about financial documents, stock prices, company fundamentals, and market data.
            """
        )
        
        # Disclaimer
        gr.HTML(
            """
            <div class="disclaimer">
                <div class="disclaimer-title">⚠️ Important Disclaimer</div>
                <div class="disclaimer-text">
                    InvestIQ provides investment research and educational information. 
                    <strong>It is not financial advice.</strong> 
                    Always verify information and consult with a qualified financial advisor 
                    before making investment decisions.
                </div>
            </div>
            """
        )
        
        # Chat interface
        chatbot = gr.Chatbot(
            label="Investment Research Chat",
            height=500,
        )
        
        with gr.Row():
            with gr.Column(scale=9):
                msg = gr.Textbox(
                    label="Your Question",
                    placeholder="Ask about stock prices, company fundamentals, or financial documents...",
                    lines=2,
                    show_label=False
                )
            with gr.Column(scale=1):
                submit_btn = gr.Button("Send", variant="primary", size="lg")
        
        with gr.Row():
            clear_btn = gr.Button("🗑️ Clear Chat", size="sm")
        
        # Example questions
        gr.Markdown("### 💡 Example Questions:")
        gr.Examples(
            examples=[
                "What was Apple's revenue according to the 10-K?",
                "What is Apple's current stock price?",
                "What are Apple's financial fundamentals?",
                "Analyze Apple as an investment opportunity",
            ],
            inputs=msg,
            label="Click an example to try it"
        )
        
        # Info section
        gr.Markdown(
            """
            ---
            
            ### 🔧 Available Data Sources
            
            - **📄 Financial Documents**: Search uploaded 10-K reports and annual filings
            - **📈 Live Stock Prices**: Get current market quotes from Alpha Vantage
            - **📊 Company Fundamentals**: P/E ratio, market cap, revenue, EPS, and more
            - **📰 Financial News**: Recent news articles with sentiment analysis
            - **📉 Historical Data**: Past stock performance and price trends
            
            ### ℹ️ Tips for Best Results
            
            - Be specific in your questions (mention company names or ticker symbols)
            - For document questions, mention "according to the 10-K" or "in the annual report"
            - For market data, specify if you want current, historical, or fundamental information
            - The agent will automatically select the appropriate tools based on your question
            
            ### ⚙️ Requirements
            
            - ✅ Ollama running with qwen3:0.6b model
            - ✅ Alpha Vantage API key in .env file (for live market data)
            - ✅ ChromaDB with financial documents (from Milestone 2)
            """
        )
        
        # Event handlers
        msg.submit(chat_with_agent, inputs=[msg, chatbot], outputs=chatbot).then(
            lambda: "", None, msg
        )
        
        submit_btn.click(chat_with_agent, inputs=[msg, chatbot], outputs=chatbot).then(
            lambda: "", None, msg
        )
        
        clear_btn.click(clear_chat, outputs=chatbot)
    
    return demo


if __name__ == "__main__":
    print("=" * 70)
    print("InvestIQ - Investment Research Assistant")
    print("=" * 70)
    print("\n🚀 Starting Gradio interface...")
    
    # Initialize agent on startup
    print("🤖 Initializing investment research agent...")
    success, msg = initialize_agent()
    if success:
        print(f"✅ {msg}")
        print(f"✅ Model: qwen3:0.6b")
        print(f"✅ Tools: {len(agent.tools)} available")
    else:
        print(f"⚠️  Warning: {msg}")
        print("⚠️  Agent will attempt to initialize when first question is asked")
    
    # Check for API key
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if api_key:
        print("✅ Alpha Vantage API key found")
    else:
        print("⚠️  Alpha Vantage API key not found (live market data will not work)")
        print("   Create .env file with ALPHA_VANTAGE_API_KEY=your_key")
    
    print("\n" + "=" * 70)
    print("🌐 Launching Gradio UI...")
    print("=" * 70)
    
    # Create and launch the UI
    demo = create_ui()
    demo.launch(
        share=False,  # Set to True for public URL (ngrok-style)
        server_name="127.0.0.1",
        server_port=7861,  # Changed to 7861 to avoid port conflict
        show_error=True
    )
