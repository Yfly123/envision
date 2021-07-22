import pandas as pd
import os
import numpy as np
res1=[]
def get_Vmax():

    file_addr = r'C:\Users\fei.yang4\Documents\work\0713-lyy-申请单\get_tem_soc\results\电性能测试资源使用计划表-全.xlsx'
    data = pd.read_excel(file_addr)
    df = pd.DataFrame(data)
    ypscbh = df['样品生产编号']
    Vmax = df['电芯max()']
    Vmin = df["电芯Vmin(V)"]
    dic1 = dict(zip(ypscbh, Vmax))
    dic2 = dict(zip(ypscbh, Vmin))
    return dic1,dic2

def add_tem_soc():
    res=[]
    dic1,dic2=get_Vmax()
    file_address = r'C:\Users\fei.yang4\Documents\WXWork\1688850869004222\Cache\File\2021-07\hisstepdata.csv'
    data = pd.read_csv(file_address)
    df = pd.DataFrame(data)
    lst = [g for _, g in df.groupby('barcode')]
    for temp in lst:
        barcode_id=temp['barcode'].to_list()

        df1=pd.DataFrame(temp)
        lst1 = [g for _, g in df1.groupby('flowid')]
        for last_group in lst1:
            flow_id = last_group['flowid'].tolist()
            tem = []
            n = 0
            end_voltage=last_group["endvoltage"].tolist()
            step_name_value=last_group["stepname"].tolist()
            chargecapacity = last_group["chargecapacity"].tolist()
            dischargecapacity = last_group["dischargecapacity"].tolist()
            stepnum = last_group["stepnum"].tolist()
            try:
                for i in range(len(step_name_value)):
                    temp1,temp2=[],[]
                    if step_name_value[i]==4:
                        if abs(int(end_voltage[i])/1e6-float(dic1[str(barcode_id[0])])) <=0.005:
                            # print(dic1[barcode_id])
                            if step_name_value[i+2]==5:
                                # print('----5-----')
                                if abs(int(end_voltage[i+2])/1e6-dic2[barcode_id[0]]) <=0.005:
                                    n += 1
                                    temp1.append(str(barcode_id[0]))
                                    temp1.append(str(flow_id[0]))
                                    temp2.append(str(barcode_id[0]))
                                    temp2.append(str(flow_id[0]))
                                    try:
                                        temp1.append(dic1[str(barcode_id[0])])
                                        temp2.append(dic2[str(barcode_id[0])])
                                    except:
                                        continue
                                    temp1.append(n)
                                    temp2.append(n)
                                    temp1.append(chargecapacity[i])
                                    temp2.append(dischargecapacity[i+2])
                                    temp1.append(stepnum[i])
                                    temp2.append(stepnum[i+2])
                                else:
                                    break
                    # print(temp1)
                    # print(temp2)
                    tem.append([temp1,temp2])
                    # tem.append(temp1)
                    # tem.append(temp2)

            except:
                # tem.append(np.nan)
                continue
            # tem.append(df1["capacity"])
        res.append(tem)
        res1.append(tem)
    df1=pd.DataFrame(res1)
    df1.to_csv('test.csv',index=False)

if __name__ == '__main__':
    add_tem_soc()
    # get_Vmax()