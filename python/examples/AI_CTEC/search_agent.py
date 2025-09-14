import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, WebSearchTool, Runner
from agents.model_settings import ModelSettings

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set. Please add it to your .env file.")

INSTRUCTIONS = (
    "You are a research assistant. Given a user question, you can decide whether to search the web "
    "to get current information. If you use the web search, summarize the results clearly and concisely. "
    "Always return the answer as a short, conversational response that a student in the CTEC robotics lab "
    "would understand. Use tags in brackets to indicate tone and emotion, because this will be used with ElevenLabs TTS. "
    "Keep answers about a 10-second spoken response. Do not include commentary about your process; only give the final answer."
)

search_agent = Agent(
    name="LiveSearchAgent",
    model="gpt-5-nano",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool()],
    model_settings=ModelSettings(
        tool_choice="auto",
        agent_type="zero-shot-react-description"
    )
)

_cache = {}

async def fetch_live_info(user_query: str) -> str:
    """Fetch live info using the zero-shot agent with caching and error handling."""
    if user_query in _cache:
        return _cache[user_query]

    try:
        result = await Runner.run(search_agent, user_query)
        _cache[user_query] = result.final_output
        return result.final_output
    except Exception as e:
        print("Error fetching live info:", e)
        return "I could not fetch live information at this time."
