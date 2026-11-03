"""数据库读写测试：建表 → 插入 → 查询 → 更新 → 删除。

使用临时表，连接关闭后自动删除，不影响数据库中已有的数据。
"""

import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="123597",
)

with conn.cursor() as cur:
    # 1. 创建临时测试表（仅在当前连接中存在，断开即自动删除）
    cur.execute(
        """
        CREATE TEMP TABLE db_test (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        );
        """
    )
    print("1. 建表成功（临时表）")

    # 2. 插入数据
    cur.executemany(
        "INSERT INTO db_test (name, score) VALUES (%s, %s);",
        [("张三", 90), ("李四", 85), ("王五", 78)],
    )
    print("2. 插入 3 条数据成功")

    # 3. 查询数据
    cur.execute("SELECT id, name, score FROM db_test ORDER BY id;")
    rows = cur.fetchall()
    assert len(rows) == 3, f"期望 3 条，实际 {len(rows)} 条"
    for row in rows:
        print(f"   {row}")
    print("3. 查询成功，数据正确")

    # 4. 更新数据
    cur.execute("UPDATE db_test SET score = 95 WHERE name = '张三';")
    cur.execute("SELECT score FROM db_test WHERE name = '张三';")
    assert cur.fetchone()[0] == 95, "更新未生效"
    print("4. 更新成功：张三 90 -> 95")

    # 5. 删除数据
    cur.execute("DELETE FROM db_test WHERE name = '王五';")
    cur.execute("SELECT COUNT(*) FROM db_test;")
    assert cur.fetchone()[0] == 2, "删除未生效"
    print("5. 删除成功：剩余 2 条数据")

conn.close()  # 连接关闭，临时表自动清理
print("\n全部测试通过！临时表已随连接关闭自动清理。")
