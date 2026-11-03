import os

from dotenv import load_dotenv

load_dotenv(override=True)

KIMI_API_KEY = os.getenv("KIMI_API_KEY") or os.getenv("SILICONFLOW_API_KEY")
KIMI_BASE_URL = (
    os.getenv("KIMI_BASE_URL")
    or os.getenv("SILICONFLOW_BASE_URL")
    or "https://api.kimi.com/coding/v1"
)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
