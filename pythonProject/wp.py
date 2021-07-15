import re
import pandas as pd
import os
import numpy as np
def get_Vmax():
    file_addr = r'C:\Users\fei.yang4\Documents\work\0713-lyy-申请单\get_tem_soc\results\电性能测试资源使用计划表-全.xlsx'
    data = pd.read_excel(file_addr)
    df = pd.DataFrame(data)
    ypscbh = df['样品生产编号'].tolist()
    Vmax = df['电芯max()'].tolist()
    Vmin = df["电芯Vmin(V)"]
    dic1 = dict(zip(ypscbh, Vmax))
    dic2 = dict(zip(ypscbh, Vmin))

def add_tem_soc():
    file_address = r'C:\Users\fei.yang4\Desktop\results\hisstepdata.xlsx'
    data = pd.read_excel(file_address)
    df = pd.DataFrame(data)
    lst = [g for _, g in df.groupby('barcode')]
    for temp in lst:
        df1=pd.DataFrame(temp)
        lst1 = [g for _, g in df1.groupby('flowid')]
        for last_group in lst1:
            n=0
            end_voltage=last_group["endvoltage"].tolist()
            step_name_value=last_group["stepname"].tolist()
            for i in range(len(step_name_value)):
                if step_name_value[i]==4:
                    if abs(int(end_voltage[i])-5.0002) <=0.005:
                        print('-----')
                        if step_name_value[i+2]==5:
                            print('----5-----')
                            if abs(int(end_voltage[i+2]-4.0002)) <=0.005:
                                n += 1
                            else:
                                break
            print(n)

if __name__ == '__main__':
    add_tem_soc()