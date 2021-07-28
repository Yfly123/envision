"""
@Time ： 2021/7/23 21:26
@Auth ： Fei.Yang
"""
import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
from sql_operation import Database_operation,pd
sql_file = 'postgre_sql.sql'#SQL语句放在该文件中
# 读取 sql 文件文本内容
def plot_pic(data):
    data.iloc[:, 0] = data.iloc[:, 0].div(1e6)
    data.iloc[:, 1] = data.iloc[:, 1].div(1e6)
    x=data.iloc[:,1].values.tolist()   #capacity,,横坐标
    y=data.iloc[:,0].values.tolist()   #voltage
    plt.plot(x,y,'g')
    plt.xlabel("Capacity/Ah")
    plt.ylabel("Voltage/V")
    plt.xlim(left=0)
    plt.savefig('test-1.jpg')
    plt.show()

if __name__=='__main__':
    do = Database_operation()
    sql = open(sql_file, 'r', encoding='utf8')
    sqltxt = sql.readlines()
    sql.close()
    sql = "".join(sqltxt)
    res=do.get_all(sql)
    data = pd.DataFrame(res)
    data =data.iloc[:,-2:]
    data.dropna(how='all',inplace=True)
    data.fillna(0,inplace=True)
    #该SQL语句查询的数据是按时间倒序，因此需要将所有数据反转
    data = data.iloc[::-1]
    data.to_excel('test-1.xlsx', index=False)
    # plot_pic(data)
