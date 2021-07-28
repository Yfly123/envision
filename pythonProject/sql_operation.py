"""
@Time ： 2021/7/21 14:02
@Auth ： Fei.Yang
"""
import pandas as pd
import psycopg2

class Database_operation():
    def __init__(self):
        # self.pg_host = "10.202.35.11"
        self.pg_host = "10.202.8.68"
        self.pg_port = "5432"
        self.pg_user = "tvc_report_qas"
        self.pg_password = "Tvc@report2020"
        self.pg_database = "tvc_report_qas"
        self.pg_table = "test_excel_electrical_c1"
    def connect(self):
        self.conn = psycopg2.connect(database=self.pg_database,user=self.pg_user,password=self.pg_password,host=self.pg_host,port=self.pg_port)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()
    def get_one(self,sql,params=()):
        self.connect()
        self.cursor.execute(sql, params)
        result = self.cursor.fetchone()
        self.close()
        return result

    def get_all(self,sql,params=()):
        self.connect()
        self.cursor.execute(sql,params)
        list1=self.cursor.fetchall()
        self.close()
        return list1

    def insert(self,sql,params=()):
        return self.__edit(sql,params)

    def update(self, sql, params=()):
        return self.__edit(sql, params)

    def delete(self, sql, params=()):
        return self.__edit(sql, params)

    def __edit(self,sql,params):
        self.connect()
        res=self.cursor.execute(sql,params)
        self.conn.commit()
        self.close()
        return res

# if __name__=='__main__':
#     do = Database_operation()
#     # sql ="INSERT INTO yf_test (att) SELECT test_excel_electrical_c1.barcode AS att FROM test_excel_electrical_c1 "
#     # sql="select cycleid_join_dz,rg FROM bi_cycle_loan_insert where barcode = '0120X0503021' order by cycleid_join_dz ASC"
#     sql_file = '123.sql'
#     # 读取 sql 文件文本内容
#     sql = open(sql_file, 'r', encoding='utf8')
#     sqltxt = sql.readlines()
#     # 此时 sqltxt 为 list 类型
#     # 读取之后关闭文件
#     sql.close()
#     # list 转 str
#     sql = "".join(sqltxt)
#     res=do.get_all(sql)
#
#     # new_colume = ['序号', '值']
#     data = pd.DataFrame(res)
#     data.fillna(0,inplace=True)
#     data.iloc[:,-2] = data.iloc[:,-2].div(1e6)
#     data.iloc[:,-1] =data.iloc[:,-1].div(1e6)
#     print(data.iloc[:,-2:])
#     data.to_excel('test.xlsx',index=False)

