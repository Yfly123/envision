#用于拆分一个EXCEL中某个列中数值相同的块到单独的EXCEL中
#相当于把一个excel拆成多个
import re
import pandas as pd
import os
import numpy as np
def add_tem_soc():
    file_address= r'C:\Users\fei.yang4\Documents\work\0713-lyy-申请单\get_tem_soc\sqd0715.xlsx'

    data=pd.read_excel(file_address)
    df=pd.DataFrame(data)
    ypbh = df["样品生产编号"]
    ypbh = ypbh.tolist()
    for i in range(len(ypbh)):
        if list(str(ypbh[i]))[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            ypbh[i] = '0' + str(ypbh[i])
    ypbh = pd.DataFrame(ypbh)
    df["样品生产编号"] = ypbh

    temp=[]
    soc=[]
    t_descri = df["测试项目细节（手动输入）"].tolist()
    t_cont = df["测试类型"].tolist()
    for i in range(len(t_cont)):
        #删选出温度
        if "℃" in str(t_cont[i]):
            temp_temp=re.findall(r"-?\d+℃",t_cont[i])
            temp_temp=temp_temp[0].replace("℃","")
            temp.append(temp_temp)
        elif "℃" in str(t_descri[i]):
            temp_temp = re.findall(r"-?\d+℃", t_descri[i])
            temp_temp = temp_temp[0].replace("℃", "")
            temp.append(temp_temp)
        else:
            temp.append(np.nan)
        #SOC数据查询
        if "%" in str(t_cont[i]):
            soc_temp=re.findall(r"\d+%",t_cont[i])
            soc_temp=soc_temp[0].replace("%","")
            soc.append(soc_temp)
        elif "%" in str(t_descri[i]):
            soc_temp = re.findall(r"\d+%", t_descri[i])
            soc_temp=soc_temp[0].replace("%","")
            soc.append(soc_temp)
        else:
            soc.append(np.nan)
    temp_soc_data=pd.DataFrame({'温度':temp,'SOC':soc})

    all_data=df.join(temp_soc_data)


    print("开始保存...")
    i =1
    os.chdir(os.path.join(file_address,'..'))
    try:  # 如果该文件不存在，则创建
        os.mkdir('results')
    except:
        print('results文件已存在，无需创建！')
    new_dir = os.path.join(os.getcwd(), 'results')
    os.chdir(new_dir)
    file_name="电性能测试资源使用计划表-全.xlsx"
    all_data.to_excel(file_name,index=False)
    print("保存结束...")

if __name__=='__main__':
    add_tem_soc()