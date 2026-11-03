# Agent Test

This project contains a LangChain agent example with simulated weather and
Tavily web search tools, using the Kimi Coding API.

## Setup

Add your Kimi Coding API key to `.env`:

```dotenv
KIMI_API_KEY=your-kimi-api-key
KIMI_BASE_URL=https://api.kimi.com/coding/v1
TAVILY_API_KEY=your-tavily-api-key
```

Install dependencies and run the example:

```powershell
uv sync
uv run agent-test
```

The agent calls the configured model and Tavily, so valid API keys and network
access are required. The weather tool itself returns a simulated sunny forecast.
The example streams the final answer as it is generated.

## Create an agent

Use `agent_test.agent_utils.create_agent` to create an agent with the configured
Kimi model:

```python
from agent_test.agent_utils import create_agent

agent = create_agent(
    tools=[get_weather],
    system_prompt="你是一个助手，你可以查询城市的天气。",
)
```

Pass `model=` when you want to use a different LangChain chat model.