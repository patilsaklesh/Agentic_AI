import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage

# Load API keys
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

system_prompt = "Act as an AI chatbot who is smart and friendly"

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt):
    # Use Groq LLM
    llm = ChatGroq(model=llm_id)

    # Add search tool only if enabled
    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    # Create the agent
    agent = create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=system_prompt
    )

    # Wrap query as a HumanMessage
    state = {"messages": [HumanMessage(content=query)]}

    # Run the agent
    response = agent.invoke(state)

    # Extract AI messages
    messages = response.get("messages", [])
    ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]

    return ai_messages[-1] if ai_messages else "No response generated."


if __name__ == "__main__":
    response = get_response_from_ai_agent(
        llm_id="llama-3.3-70b-versatile",
        query="Hello! Who won the 2022 FIFA World Cup?",
        allow_search=True,
        system_prompt=system_prompt
    )
    print("🤖 AI Agent:", response)
