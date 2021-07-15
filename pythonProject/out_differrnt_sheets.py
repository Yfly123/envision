#用于拆分一个EXCEL中某个列中数值相同的块到单独的EXCEL中
#相当于把一个excel拆成多个

import pandas as pd
import os
def dissemble():
    file_address= r'C:\Users\fei.yang4\Desktop\results\ACR_OCV_汇总总表 .xlsx'

    data=pd.read_excel(file_address)
    df=pd.DataFrame(data)

    print(df.columns.values)
    lst = [g for _, g in df.groupby('订单号')]
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
        ddh = part_data["订单号"].values[0]
        file_name="{}.xlsx".format(ddh)
        part_data.to_excel(file_name)
        i += 1
if __name__=='__main__':
    dissemble()