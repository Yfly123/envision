import psycopg2
import pandas as pd

pg_host = "10.202.35.11"
pg_port = "5432"
pg_user = "Datalake"
pg_password = "Datalake"
pg_database = "tvc"
pg_table = "test_excel_electrical_c1"

conn_string = "host=" + pg_host + " port=" + pg_port + " dbname=" + pg_database + " user=" + pg_user + " password=" + pg_password
conn = psycopg2.connect(conn_string)
curs = conn.cursor()

sql_command = "select * from bi_cycle_loan_insert"

# try:
#     data1 = pd.read_sql(sql_command, conn)
#     print( data1 )
# except:
#     print("load data from postgres failure !")
#     exit()
#
# if data1.shape[0] == 0:
#     print("there is no data in !")



data1 = pd.read_sql(sql_command, conn)
df = pd.DataFrame(data1)
# print( data1 )
list1 = [g for _,g in data1.groupby('test_type')]
print( list1 )