from langchain_openai import ChatOpenAI

from agent_test.env_utils import KIMI_API_KEY, KIMI_BASE_URL

if not KIMI_API_KEY:
    raise ValueError("KIMI_API_KEY is required; set it in .env.")

kimi_llm = ChatOpenAI(
    api_key=KIMI_API_KEY,
    base_url=KIMI_BASE_URL,
    model="kimi-for-coding",
)
