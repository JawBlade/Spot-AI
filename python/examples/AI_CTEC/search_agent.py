import logging
import os
from dotenv import load_dotenv
from agents import Agent, WebSearchTool, Runner
from agents.model_settings import ModelSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY is not set. Please add it to your .env file.")
    raise ValueError("OPENAI_API_KEY is not set. Please add it to your .env file.")

INSTRUCTIONS = (
    "You are a research assistant. Follow these rules when answering questions:"
    "1. Decide first if the question needs a web search to get current information. If not, answer directly. "
    "2. Always give a short, clear, and conversational response that anyone can easily understand. "
    "3. Keep your answer about the length of a 10-second spoken response (around 2–3 sentences max). "
    "4. Add tone and emotion tags in brackets (e.g., [cheerful], [thoughtful]) for use with ElevenLabs TTS. "
    "5. Never explain your process, reasoning, or mention web searching—only give the final answer. "
    "6. Avoid filler words or long explanations. Focus only on what the user needs to know right now. "
    "Goal: Provide concise, friendly, and accurate answers that sound natural when spoken aloud."
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
        logger.info("Returning cached result for query.")
        return _cache[user_query]

    try:
        logger.info(f"Fetching live info for query: {user_query}")
        result = await Runner.run(search_agent, user_query)
        _cache[user_query] = result.final_output
        logger.info("Fetched and cached live info.")
        return result.final_output
    except Exception as e:
        logger.error(f"Error fetching live info: {e}")
        return "Sorry, I couldn't fetch live information right now."
