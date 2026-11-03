import psycopg
from langchain_tavily import TavilySearch
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from pydantic import BaseModel, Field

from agent_test.agent_utils import create_agent
from agent_test.chat_history import init_chat_table, save_message
from agent_test.env_utils import TAVILY_API_KEY


def get_weather(city: str) -> str:
    """获取给定城市的天气。"""
    return f"{city} 天气晴朗！"

# Agent回答内容引用的网页信息
class Reference(BaseModel):
    title: str = Field(description="The title of the web page cited in the answer")
    url: str = Field(description="The url of the web page cited in the answer")

# Agent的回答内容
class AnswerInfo (BaseModel):
    answer: str = Field(description="The final answer for user")
    reference: list[Reference] = Field(description="The web pages cited in the answer")
    should_exit: bool = Field(
        description="Whether the user wants to end the entire conversation"
    )
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is required; set it in .env.")

web_search = TavilySearch(
    tavily_api_key=TAVILY_API_KEY,
    max_results=5,
    include_raw_content=False,
)

pg_conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="agent_test",
    user="postgres",
    password="123597",
    autocommit=True,
)
checkpointer = PostgresSaver(
    conn=pg_conn,
    serde=JsonPlusSerializer(
        allowed_msgpack_modules=[
            (AnswerInfo.__module__, AnswerInfo.__name__),
            (Reference.__module__, Reference.__name__),
        ]
    ),
)
checkpointer.setup()  # 首次运行自动建表，重复执行无副作用
init_chat_table(pg_conn)  # 原始文本对话记录表

agent = create_agent(
    tools=[get_weather, web_search],
    system_prompt=(
        "你是一个助手。get_weather 是模拟天气工具，tavily_search 用于联网搜索。"
        "需要最新、实时或不在已有知识中的信息时，使用 tavily_search。"
        "根据搜索结果回答，并附上来源链接；未使用搜索时，reference 返回空列表。"
        "如果用户的语义是结束整段对话、退出程序或不再继续聊天，"
        "将 should_exit 设为 true，直接简短告别，无需调用工具；否则设为 false。"
        "用户只是要求结束某项任务或讨论与结束有关的话题时，不要退出。"
    ),
    response_format=AnswerInfo,
    checkpointer=checkpointer,
)


def main() -> None:
    thread_id = "quick-start"
    config = {"configurable": {"thread_id": thread_id}}

    print("开始对话，输入“退出”、exit 或 quit 结束。")
    while True:
        try:
            question = input("\n用户：").strip()
        except (EOFError, 6):
            print("\n对话结束。")
            break

        if not question:
            continue
        if question == "退出" or question.lower() in {"exit", "quit"}:
            print("对话结束。")
            break

        save_message(pg_conn, thread_id, "user", question)

        answer_info: AnswerInfo | None = None
        for state in agent.stream(
            {"messages": [{"role": "user", "content": question}]},
            config=config,
            stream_mode="values",
        ):
            if isinstance(state.get("structured_response"), AnswerInfo):
                answer_info = state["structured_response"]

        if answer_info is None:
            raise RuntimeError("Agent did not return a structured response.")

        print(f"助手：{answer_info.answer}")
        save_message(
            pg_conn,
            thread_id,
            "assistant",
            answer_info.answer,
            sources=[r.model_dump() for r in answer_info.reference],
        )
        if answer_info.reference:
            print("参考来源：")
            for reference in answer_info.reference:
                print(f"- {reference.title}: {reference.url}")

        if answer_info.should_exit:
            print("对话结束。")
            break


if __name__ == "__main__":
    main()
