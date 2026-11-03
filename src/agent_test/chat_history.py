"""把对话消息以原始文本存入 PG，方便直接用 SQL 查看。

checkpoint 表是 LangGraph 内部状态（msgpack 二进制），
本模块额外维护一份可读的对话记录。
"""

import json

import psycopg

DDL = """
CREATE TABLE IF NOT EXISTS chat_messages (
    id BIGSERIAL PRIMARY KEY,
    thread_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    sources JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""


def init_chat_table(conn: psycopg.Connection) -> None:
    conn.execute(DDL)


def save_message(
    conn: psycopg.Connection,
    thread_id: str,
    role: str,
    content: str,
    sources: list[dict] | None = None,
) -> None:
    conn.execute(
        "INSERT INTO chat_messages (thread_id, role, content, sources)"
        " VALUES (%s, %s, %s, %s);",
        (thread_id, role, content, json.dumps(sources) if sources else None),
    )
