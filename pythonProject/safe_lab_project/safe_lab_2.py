"""
@Time ： 2021/7/22 12:57
@Auth ： Fei.Yang
"""
# -*- coding: utf-8 -*-
import datetime
import logging
import re

import pandas as pd
import os
import numpy as np
import datetime as dt
class Data_process():
    def __init__(self):
        #将待处理的文件放在
        self.root_addr=r'C:\Users\fei.yang4\Documents\work\safety_lab'
        self.input_addr = r"C:\Users\fei.yang4\Documents\work\safety_lab\input\step_data"
        self.sensor_addr = r'C:\Users\fei.yang4\Documents\work\safety_lab\input\stress_sensor_data\11-2020.csv'
            # r"C:\Users\fei.yang4\Documents\work\safety_lab\input\stress_sensor_data"
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
        # new_data内格式为    '循环序号','充电容量(Ah)', '放电容量(Ah)','起始时间'
        return new_data

    # 筛选并合并表格中数据形成新的数据表(循环数据表和工步数据表)
    def intergrate_data(self):
        cycle_data = self.choose_data_from_sheet('循环数据表',['充电容量(Ah)','放电容量(Ah)','循环序号'])
        step_data = self.choose_data_from_sheet('工步数据表',['循环号','绝对时间'])
        os.chdir(self.root_addr+'/output')
        with pd.ExcelWriter('cycle_step_datas.xlsx') as writer:
            cycle_data.to_excel(writer, sheet_name='循环数据表',index=False)
            step_data.to_excel(writer, sheet_name='工步数据表',index=False)
        logging.info("循环数据表-工步数据表数据重整成功！")



#根据所给时间在pressure数据文件中找到与该时间差最近的数据的索引
    def find_press_pos_of_step_num(self,time1):
        #找该时间所保存的压力数据所在的文件
        sensor_data_addr = os.path.join(os.getcwd(),'..')+'\stress_sensor_data'
        os.chdir(sensor_data_addr)
        temp = re.findall(r'2\d{3}?', str(time1))
        for dirpath, dirnames, filenames in os.walk(sensor_data_addr):
            for file_name in filenames:
                if file_name.endswith('.csv') and str(temp[0]) in file_name:
                    csv_addr = os.path.join(dirpath,file_name)
                    data1 = pd.read_csv(csv_addr)
                    data = [time1] * len(data1['Datetime'])
                    data = pd.to_datetime(data)
                    new_df = (pd.to_datetime(data1['Datetime']) - data)
                    new_df = pd.to_timedelta(abs(new_df))
                    min_data = new_df.min()
                    min_data = pd.to_timedelta(min_data)
                    pos = new_df[new_df == min_data].index.tolist()
                    return pos[0]

    #输入数据为开始时间集,获取相邻时间戳直接传感器数据值
    def search_pressure_data(self, data_summary):
        pos=[]
        for i in range(len(data_summary)):
            time_data = data_summary.at[i, '起始时间']
            self.find_press_pos_of_step_num(str(time_data))
            pos.append(self.find_press_pos_of_step_num(str(time_data)))
            # if len(pos)>=2:
            #     pass
            print(pos)

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
    # # dp.intergrate_data()
    res = dp.get_start_time_and_cycle_num()
    dp.search_pressure_data(res)
    # #获取每个起始时间的年，然后再去对应的年的压力文件里找数据



    # res = dp.find_press_pos_of_step_num('2020/11/20  18:03:51')
    # print(res)
