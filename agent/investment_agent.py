"""
Investment Research Agent
Uses LangGraph and ChatOllama to create an intelligent investment research assistant.
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Import all tools
from tools.financial_document_tool import search_financial_documents
from tools.alpha_vantage_tools import (
    get_live_stock_price,
    get_historical_stock_data,
    get_company_fundamentals,
    get_financial_news_sentiment
)


# Define the agent state
class AgentState(TypedDict):
    """State for the investment research agent."""
    messages: Annotated[Sequence[BaseMessage], "The messages in the conversation"]


class InvestmentResearchAgent:
    """
    Investment Research Agent that helps users research investments.
    
    Capabilities:
    - Search financial documents (10-K, annual reports)
    - Get live stock prices
    - Analyze historical price data
    - Review company fundamentals
    - Check recent news and sentiment
    
    The agent intelligently selects which tools to use based on the user's question.
    """
    
    def __init__(self, model_name: str = "qwen2.5:7b"):
        """
        Initialize the Investment Research Agent.
        
        Args:
            model_name: Ollama model name (default: qwen2.5:7b)
        """
        self.model_name = model_name
        
        # Initialize LLM with optimized settings
        self.llm = ChatOllama(
            model=self.model_name,
            base_url="http://localhost:11434",  # Explicit Ollama server URL
            temperature=0,  # Zero temperature for fastest, most deterministic responses
            num_predict=512,  # Limit response length for speed
        )
        
        # Define available tools
        self.tools = [
            search_financial_documents,
            get_live_stock_price,
            get_historical_stock_data,
            get_company_fundamentals,
            get_financial_news_sentiment
        ]
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Create tool node
        self.tool_node = ToolNode(self.tools)
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow for the agent."""
        
        # Define the function that calls the model
        def call_model(state: AgentState):
            messages = state["messages"]
            response = self.llm_with_tools.invoke(messages)
            return {"messages": [response]}
        
        # Define the function that determines whether to continue or end
        def should_continue(state: AgentState):
            messages = state["messages"]
            last_message = messages[-1]
            
            # If there are no tool calls, then we finish
            if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
                return "end"
            # Otherwise, we continue
            else:
                return "continue"
        
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", call_model)
        workflow.add_node("tools", self.tool_node)
        
        # Set entry point
        workflow.set_entry_point("agent")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "continue": "tools",
                "end": END
            }
        )
        
        # Add edge from tools back to agent
        workflow.add_edge("tools", "agent")
        
        # Compile the graph (recursion limit handled by LangGraph internally)
        return workflow.compile()
    
    def run(self, user_query: str) -> str:
        """
        Run the agent with a user query.
        
        Args:
            user_query: The user's question or request
        
        Returns:
            The agent's response as a string
        """
        # Shorter, focused system message for speed
        system_message = """Answer using ONE tool only.

For "10-K" or "revenue" questions: use search_financial_documents ONLY.
For "stock price" questions: use get_live_stock_price ONLY.

Call ONE tool, then answer immediately. NO multiple tools."""
        
        # Create initial messages
        messages = [
            HumanMessage(content=system_message),
            HumanMessage(content=user_query)
        ]
        
        # Run the graph
        result = self.graph.invoke({"messages": messages})
        
        # Extract the final response
        final_messages = result["messages"]
        
        # Get the last AI message
        for message in reversed(final_messages):
            if isinstance(message, AIMessage):
                return message.content
        
        return "I apologize, but I couldn't generate a response. Please try again."
    
    def stream(self, user_query: str):
        """
        Stream the agent's response (for future UI integration).
        
        Args:
            user_query: The user's question
        
        Yields:
            Chunks of the response
        """
        # Add system message
        system_message = """You are InvestIQ, an expert investment research assistant."""
        
        messages = [
            HumanMessage(content=system_message),
            HumanMessage(content=user_query)
        ]
        
        # Stream the response
        for chunk in self.graph.stream({"messages": messages}):
            yield chunk


def create_investment_agent(model_name: str = "qwen2.5:7b") -> InvestmentResearchAgent:
    """
    Factory function to create an InvestmentResearchAgent.
    
    Args:
        model_name: Ollama model to use (default: qwen2.5:7b)
    
    Returns:
        Configured InvestmentResearchAgent instance
    """
    return InvestmentResearchAgent(model_name=model_name)


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("InvestIQ - Investment Research Agent")
    print("=" * 60)
    print("\nInitializing agent...")
    
    try:
        agent = create_investment_agent()
        print("✓ Agent initialized successfully")
        print(f"✓ Using model: qwen2.5:7b")
        print(f"✓ Available tools: {len(agent.tools)}")
        print("\nAgent is ready to answer investment research questions.")
        print("\nExample questions:")
        print("  - What is Apple's current stock price?")
        print("  - What was the company's revenue according to the 10-K?")
        print("  - Analyze Tesla as an investment")
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"✗ Error initializing agent: {e}")
