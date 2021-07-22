#用于拆分一个EXCEL中某个列中数值相同的块到单独的EXCEL中
#相当于把一个excel拆成多个

import pandas as pd
import os
def dissemble():
    file_address= r'C:\Users\fei.yang4\Documents\work\0716_file_deal\HD存储汇总0716new.xlsx'

    data=pd.read_excel(file_address)
    df=pd.DataFrame(data)
    # scbh=df["生产编号"]
    # scbh=scbh.tolist()
    # for i in range(len(scbh)):
    #     if list(str(scbh[i]))[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
    #         scbh[i]='0'+str(scbh[i])
    # scbh=pd.DataFrame(scbh)
    # print(df.columns.values)
    # df["生产编号"]=scbh
    #处理时间
    set_index=['测试申请单号','测试编号','生产编号','电压(v)','内阻(mΩ)','记录人','日期','备注']
    t_date = df["日期 "]
    t_date = pd.to_datetime(t_date)
    df["日期 "]=t_date.apply((lambda  x:x.date()))

    lst = [g for _, g in df.groupby('测试申请单号')]

    print("开始保存...")
    i =1
    os.chdir(os.path.join(file_address,'..'))
    try:  # 如果该文件不存在，则创建
        os.mkdir('results')
    except:
        print('results文件已存在，无需创建！')
    new_dir = os.path.join(os.getcwd(), 'results')
    os.chdir(new_dir)
    for part_data in lst:
        print("共%s,处理了%s..."%(len(lst),i))
        ddh = part_data["测试申请单号"].values[0]
        file_name="{}.xlsx".format(ddh)
        part_data.to_excel(file_name,index=False,header=set_index)
        i += 1
if __name__=='__main__':
    dissemble()