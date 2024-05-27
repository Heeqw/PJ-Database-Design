import mysql.connector

# MySQL 连接信息
config = {
    'host': 'localhost',
    'user': 'admin',
    'password': '123456',
    'database': 'food_ordering_system',
}

# 连接到 MySQL 数据库
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# 打开一个文件用于写入 Markdown 内容
with open('table_structure.md', 'w', encoding='utf-8') as file:
    # 获取数据库中所有表名
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    # 保存表结构说明到 Markdown 文件
    for table_name in tables:
        table_name = table_name[0]
        file.write(f"# Table: {table_name}\n\n")
        cursor.execute(f"DESCRIBE {table_name};")
        columns = cursor.fetchall()

        # 写入表格头
        file.write("| Field | Type | Null | Key | Default | Extra |\n")
        file.write("| --- | --- | --- | --- | --- | --- |\n")

        # 写入表格内容
        for column in columns:
            file.write("| " + " | ".join(str(value) if value is not None else '' for value in column) + " |\n")

        file.write("\n")

# 关闭数据库连接
cursor.close()
conn.close()
