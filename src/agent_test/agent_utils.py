from collections.abc import Callable, Sequence
from typing import Any

from langchain.agents import create_agent as langchain_create_agent
from langchain.agents.structured_output import ResponseFormat
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph


def create_agent(
    tools: Sequence[BaseTool | Callable[..., Any] | dict[str, Any]],
    system_prompt: str,
    model: str | BaseChatModel | None = None,
    response_format: ResponseFormat[Any] | type[Any] | dict[str, Any] | None = None,
    checkpointer: BaseCheckpointSaver | None = None,
) -> CompiledStateGraph:
    if model is None:
        from agent_test.my_llm import kimi_llm

        model = kimi_llm

    return langchain_create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt,
        response_format=response_format,
        checkpointer=checkpointer,
    )
