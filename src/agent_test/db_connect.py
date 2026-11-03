import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="postgres",  # 默认数据库，之后可换成你自己的库
    user="postgres",
    password="123597",  # 替换为安装 PostgreSQL 时设置的密码
)

with conn.cursor() as cur:
    cur.execute("SELECT version();")
    print(cur.fetchone())

conn.close()
