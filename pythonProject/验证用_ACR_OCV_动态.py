"""
@Time ： 2021/7/24 0:24
@Auth ： Fei.Yang
"""
import matplotlib.pyplot as plt
import xlwings as xw
from pylab import *
file_addr=r'C:\Users\fei.yang4\Documents\work\ACR_OCV_TEST.xlsx'
mpl.rcParams['font.sans-serif'] = ['SimHei']
from sql_operation import Database_operation,pd

def plot_pic(data):
    x1=data.iloc[:,1].values.tolist()   #capacity,,横坐标
    y1=data.iloc[:,0].values.tolist()   #voltage
    y2=data.iloc[:,2].values.tolist()
    x2=data.iloc[:,3].values.tolist()
    y3=data.iloc[:,4].values.tolist()
    x3=data.iloc[:,5].values.tolist()
    y4=data.iloc[:,6].values.tolist()
    x4=data.iloc[:,7].values.tolist()
    y5=data.iloc[:,8].values.tolist()
    x5=data.iloc[:,9].values.tolist()
    y6 = data.iloc[:, 10].values.tolist()
    x6 = data.iloc[:, 11].values.tolist()
    plt.plot(x1,y1,'g',label='022080601243 Charge')
    plt.plot(x2,y2,'r',label='022080601243 Discharge')
    plt.plot(x3, y3, 'y',label='022080601155 Charge')
    plt.plot(x4, y4, 'b',label='022080601155 Discharge')
    plt.plot(x5, y5, 'm',label='022080601143 Charge')
    plt.plot(x6, y6, 'c',label='022080601143 Discharge')
    plt.title("Dynamic SOC-OCV")
    plt.legend(loc=7)#图例及位置： 1右上角，2 左上角 loc函数可不写 0为最优 ncol为标签有几列,此处若是不写plt.legend，则不会显示标签

    plt.xlabel("Capacity/Ah")
    plt.ylabel("Voltage/V")
    plt.xlim(left=0)
    # plt.ylim(bottom=0)
    plt.savefig('test.jpg')
    plt.show()
    plt.close()

if __name__=='__main__':

    res=pd.read_excel(file_addr)

    data = pd.DataFrame(res)
    plot_pic(data)

    data.to_excel('test.xlsx',index=False)
    app = xw.App(visible=False,add_book=False)
    wb = app.books.open('test.xlsx')
    wb.save()
    wb.close()
    app.quit()