from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

from postgre-sql.py import Database_operation
def job_need_do():

    do = Database_operation()
        # sql ="INSERT INTO yf_test (att) SELECT test_excel_electrical_c1.barcode AS att FROM test_excel_electrical_c1 "
        # sql="select cycleid_join_dz,rg FROM bi_cycle_loan_insert where barcode = '0120X0503021' order by cycleid_join_dz ASC"
    sql_file = '123.sql'
    # 读取 sql 文件文本内容
    sql = open(sql_file, 'r', encoding='utf8')
    sqltxt = sql.readlines()
    # 此时 sqltxt 为 list 类型
    # 读取之后关闭文件
    sql.close()
    # list 转 str
    sql = "".join(sqltxt)
    res = do.insert(sql)





schd = BlockingScheduler()
schd.add_job(job_need_do,'interval',seconds=15)
#day_of_week='mon-fri',hour=9,minute=30
schd.start()
