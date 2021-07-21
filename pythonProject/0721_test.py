"""
@Time ： 2021/7/21 14:02
@Auth ： Fei.Yang
"""
import pymysql
class Database_test():
    def __init__(self):
        self.port = '3306'
        self.user = 'fei.yang'
        self.password ='123456'
        self.host='localhost'
        self.database='Test'
    def connect(self):
        self.conn = pymysql.connect(host=self.host,database=self.database,port=self.port,user=self.user,password=self.password)
        self.cursor = self.conn.cursor()
    def close(self):
        self.conn.close()
        self.cursor.close()
    def get_one(self,sql,par=()):
        self.connect()
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        self.close()
        return res
if __name__=='__main__':
    dt = Database_test()
    sql="select * from yf_test"
    res = dt.get_one(sql)
    print(res)