# sql文件夹路径
# sql_path = 'C:\\Users\\fei.yang4\\Documents\\Python_resposity\\pythonProject\\234\\123.sql\\'

# sql文件名， .sql后缀的
sql_file = '../123.sql'

# 读取 sql 文件文本内容
sql = open(sql_file, 'r', encoding='utf8')
sqltxt = sql.readlines()
# 此时 sqltxt 为 list 类型

# 读取之后关闭文件
sql.close()

# list 转 str
sql = "".join(sqltxt)

import pandas as pd
import pymysql
import psycopg2

pg_host = "10.202.35.11"
pg_port = "5432"
pg_user = "Datalake"
pg_password = "Datalake"
pg_database = "tvc"
# pg_table = "test_excel_electrical_c1"

conn_string = "host=" + pg_host + " port=" + pg_port + " dbname=" + pg_database + " user=" + pg_user + " password=" + pg_password
conn = psycopg2.connect(conn_string)
curs = conn.cursor()

curs.execute(sql)
conn.commit()

# df = pd.read_sql(sql, conn)
conn.close()

#  con为数据库连接设置，参考以下链接
#  https://blog.csdn.net/zyq_victory/article/details/78153404

# 结果就是将自己写的 sql 提取的数据读取为 DataFrame
