"""
@Time ： 2021/7/21 14:02
@Auth ： Fei.Yang
"""
# -*- coding: utf-8 -*-
# coding: utf-8
import datetime
import logging
import pandas as pd
import os
import numpy as np
import datetime as dt
class Data_process():
    def __init__(self):
        #将待处理的文件放在
        self.root_addr=r'C:\Users\fei.yang4\Documents\work\safety_lab'
        self.input_addr = r"C:\Users\fei.yang4\Documents\work\safety_lab\input\step_data"
        self.sensor_addr = r"C:\Users\fei.yang4\Documents\work\safety_lab\input\stress_sensor_data"
        self.make_file_and_log()
        logging.basicConfig(level=logging.INFO, filename='.\logs\log-'+datetime.datetime.now().strftime('%Y-%m-%d')+'.txt',filemode='a',format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',encoding='utf-8')
            # formate设置输出格式，年月日分秒毫秒，行数，等级名，打印的信息
        logging.info("logs_output文件夹创建成功！")

    #根据循环号获取对应的循环号、充电容量、放电容量
    #接口：循环号   输出：循环号对应的  充电容量、 放电容量数据
    def get_data_from_cyclenum(self,cycle_num):
        input_addr = self.root_addr+'\output\cycle_step_datas.xlsx'
        data = pd.read_excel(input_addr, sheet_name="循环数据表")
        df = pd.DataFrame(data)
        try:
            new_data = df[['循环序号', '充电容量(Ah)', '放电容量(Ah)']]
            res_data = new_data.loc[lambda new_data: new_data['循环序号'] == cycle_num, :]
            return res_data
        except:
            logging.error("检查循环数据表中是否有“循环号、充电容量、放电容量”字段")


    #输入提取表格名，所需提取表格内的字段
    def choose_data_from_sheet(self,sheet_na,need_li):
        os.chdir(self.input_addr)
        back_data=pd.DataFrame()
        for dirpath, dirnames, filenames in os.walk(os.getcwd()):
            for file_name in filenames[0:1]:
                if file_name.endswith('.xlsx') or file_name.endswith('xls') or file_name.endswith('xlsm'):
                    temp_data = pd.read_excel(file_name,sheet_name=sheet_na)
                    temp_data = pd.DataFrame(temp_data)
                    res_data = temp_data.loc[:,lambda temp_data:need_li]
                    back_data = pd.concat([back_data,res_data])
        return back_data

    #获取每张表中每个循环对应的开始时间，循环号
    def get_start_time_and_cycle_num(self):
        cycle_data = self.choose_data_from_sheet('循环数据表', ['循环序号','充电容量(Ah)', '放电容量(Ah)'])
        step_data = self.choose_data_from_sheet('工步数据表', ['循环号', '绝对时间'])
        start_data = step_data.groupby('循环号').first()
        start_data=start_data.values
        start_data=pd.DataFrame(start_data,columns=["起始时间"])
        new_data = pd.concat([cycle_data,start_data],axis=1)
        print(new_data)
        # new_data内格式为    '循环序号','充电容量(Ah)', '放电容量(Ah)','起始时间'

    # 筛选并合并表格中数据形成新的数据表(循环数据表和工步数据表)
    def intergrate_data(self):
        cycle_data = self.choose_data_from_sheet('循环数据表',['充电容量(Ah)','放电容量(Ah)','循环序号'])
        step_data = self.choose_data_from_sheet('工步数据表',['循环号','绝对时间'])
        os.chdir(self.root_addr+'/output')
        with pd.ExcelWriter('cycle_step_datas.xlsx') as writer:
            cycle_data.to_excel(writer, sheet_name='循环数据表',index=False)
            step_data.to_excel(writer, sheet_name='工步数据表',index=False)
        logging.info("循环数据表-工步数据表数据重整成功！")

    #在文件里创建output文件以及log.txt
    def make_file_and_log(self):
        self.change_dir()
        try:
            os.mkdir('logs')
            os.mkdir('output')
        except:
            print('output文件存在，无需创建！')

    #更改路径
    def change_dir(self):
        try:
            os.chdir(self.root_addr)
        except:
            print('路径更改失败，检查文件路径')
            logging.error('路径更改失败，检查文件路径')

if __name__=='__main__':
    dp = Data_process()
    # dp.intergrate_data()
    dp.get_start_time_and_cycle_num()
    # print(dp.get_data_from_cyclenum(8))



    # j = 1
    # inputdir = ''#源文件地址
    # for root, dirs, files in os.walk(inputdir):
    #     for name in files:
    #         path = [os.path.join(root, name)]
    #         if path[0].endswith(".csv"):
    #             PZL = pd.read_csv(path[0], sep=',', encoding="gbk")
    #             PZL.columns = ['Datetime', 'Ch1', 'Ch2', 'Ch3', 'Ch4']
    #             PZL['Datetime'] = pd.to_datetime(PZL['Datetime'])
    #             PZL['Ch1'] = pd.to_numeric(PZL['Ch1'], errors='coerce')
    #             PZL['Ch2'] = pd.to_numeric(PZL['Ch2'], errors='coerce')
    #             PZL['Ch3'] = pd.to_numeric(PZL['Ch3'], errors='coerce')
    #             PZL['Ch4'] = pd.to_numeric(PZL['Ch4'], errors='coerce')
    #             PZL['F'] = PZL['Ch1'] + PZL['Ch2'] + PZL['Ch3'] + PZL['Ch4']
    # for root, dirs, files in os.walk(inputdir):
    #     for name in files:
    #         path = [os.path.join(root, name)]
    #         if path[0].endswith(".xlsx"):
    #             df = pd.read_excel(path[0], sheet_name='工步数据表')
    #             a_list = df['循环号'].drop_duplicates().values.tolist()
    #             df0 = df.loc[df['循环号'] == a_list[len(a_list) - 1]]
    #             if len(df0) < 4:
    #                 df = df.drop(index=(df.loc[(df['循环号'] == a_list[len(a_list) - 1])].index))
    #                 a_list.pop()
    #             dfcap = pd.read_excel(path[0], sheet_name='循环数据表')
    #             dfcap = dfcap[['循环序号', '充电容量(Ah)', '放电容量(Ah)']]
    #             dfcap = dfcap.rename(columns={'循环序号': '循环号'})
    #             df = df[['循环号', '绝对时间']]
    #             df['绝对时间'] = pd.to_datetime(df['绝对时间'])
    #             a = df.iat[0, 1]
    #             b = df.iat[len(df) - 1, 1]
    #             b = b + datetime.timedelta(minutes=30)
    #             df.iat[len(df) - 1, 1] = b
    #             for j in range(len(PZL)):
    #                 c = (a - PZL.iat[j, 0]).total_seconds()
    #                 if c <= 0:
    #                     time1 = j
    #                     break
    #             for k in range(time1, len(PZL)):
    #                 d = (b - PZL.iat[k, 0]).total_seconds()
    #                 if d <= 0:
    #                     break
    #             PZL1 = PZL.iloc[time1:k, ]
    #             PZL1 = PZL1.reset_index(drop=True)
    #             PZL1['循环号'] = 1
    #             shouhang = df.groupby(['循环号']).first()
    #             df1 = shouhang.reset_index()
    #             df1 = df1.append(df.iloc[len(df) - 1,])
    #             df1 = df1.reset_index(drop=True)
    #             l = 0
    #             for m in range(0, len(df1) - 1):
    #                 for n in range(l, len(PZL1)):
    #                     c = df1.iat·[m, 0]
    #                     d = (PZL1.iat[n, 0] - df1.iat[m + 1, 1]).total_seconds()
    #                     if (d <= 0):
    #                         PZL1.iat[n, 6] = c
    #                     else:
    #                         l = n
    #                         break
    #             df2 = PZL1[['循环号', 'F']]
    #             Fmax = df2.groupby(['循环号']).max()
    #             Fmax = Fmax.reset_index()
    #             Fmax = Fmax.rename(columns={'F': 'F_Max'})
    #             Fmin = df2.groupby(['循环号']).min()
    #             Fmin = Fmin.reset_index()
    #             Fmin = Fmin.rename(columns={'F': 'F_Min'})
    #             Ffinal = pd.merge(Fmax, Fmin, on='循环号')
    #             Ffinal = pd.merge(Ffinal, dfcap, on='循环号')
    #             writer = pd.ExcelWriter(
    #                 r'C:\Users\zhengyu.tang\Desktop\膨胀力数据处理例子\内部数据处理脚本\output\{}_PZL.xlsx'.format(name[:-5]))
    #             Ffinal.to_excel(writer, sheet_name='PZL', index=False)
    #             if a_list[len(a_list) - 1] > 50:
    #                 for k in range(50, len(a_list) + 1, 50):
    #                     PZL2 = PZL1.loc[PZL1['循环号'] == k]
    #                     PZL2.to_excel(writer, sheet_name='{}'.format(k), index=None)
    #             writer.save()

