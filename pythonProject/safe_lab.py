# -*- coding: utf-8 -*-
# coding: utf-8

import pandas as pd
import os
import datetime

j = 1
inputdir = ''#源文件地址
for root, dirs, files in os.walk(inputdir):
    for name in files:
        path = [os.path.join(root, name)]
        if path[0].endswith(".csv"):
            PZL = pd.read_csv(path[0], sep=',', encoding="gbk")
            PZL.columns = ['Datetime', 'Ch1', 'Ch2', 'Ch3', 'Ch4']
            PZL['Datetime'] = pd.to_datetime(PZL['Datetime'])
            PZL['Ch1'] = pd.to_numeric(PZL['Ch1'], errors='coerce')
            PZL['Ch2'] = pd.to_numeric(PZL['Ch2'], errors='coerce')
            PZL['Ch3'] = pd.to_numeric(PZL['Ch3'], errors='coerce')
            PZL['Ch4'] = pd.to_numeric(PZL['Ch4'], errors='coerce')
            PZL['F'] = PZL['Ch1'] + PZL['Ch2'] + PZL['Ch3'] + PZL['Ch4']
for root, dirs, files in os.walk(inputdir):
    for name in files:
        path = [os.path.join(root, name)]
        if path[0].endswith(".xlsx"):
            df = pd.read_excel(path[0], sheet_name='工步数据表')
            a_list = df['循环号'].drop_duplicates().values.tolist()
            df0 = df.loc[df['循环号'] == a_list[len(a_list) - 1]]
            if len(df0) < 4:
                df = df.drop(index=(df.loc[(df['循环号'] == a_list[len(a_list) - 1])].index))
                a_list.pop()
            dfcap = pd.read_excel(path[0], sheet_name='循环数据表')
            dfcap = dfcap[['循环序号', '充电容量(Ah)', '放电容量(Ah)']]
            dfcap = dfcap.rename(columns={'循环序号': '循环号'})
            df = df[['循环号', '绝对时间']]
            df['绝对时间'] = pd.to_datetime(df['绝对时间'])
            a = df.iat[0, 1]
            b = df.iat[len(df) - 1, 1]
            b = b + datetime.timedelta(minutes=30)
            df.iat[len(df) - 1, 1] = b
            for j in range(len(PZL)):
                c = (a - PZL.iat[j, 0]).total_seconds()
                if c <= 0:
                    time1 = j
                    break
            for k in range(time1, len(PZL)):
                d = (b - PZL.iat[k, 0]).total_seconds()
                if d <= 0:
                    break
            PZL1 = PZL.iloc[time1:k, ]
            PZL1 = PZL1.reset_index(drop=True)
            PZL1['循环号'] = 1
            shouhang = df.groupby(['循环号']).first()
            df1 = shouhang.reset_index()
            df1 = df1.append(df.iloc[len(df) - 1,])
            df1 = df1.reset_index(drop=True)
            l = 0
            for m in range(0, len(df1) - 1):
                for n in range(l, len(PZL1)):
                    c = df1.iat[m, 0]
                    d = (PZL1.iat[n, 0] - df1.iat[m + 1, 1]).total_seconds()
                    if (d <= 0):
                        PZL1.iat[n, 6] = c
                    else:
                        l = n
                        break
            df2 = PZL1[['循环号', 'F']]
            Fmax = df2.groupby(['循环号']).max()
            Fmax = Fmax.reset_index()
            Fmax = Fmax.rename(columns={'F': 'F_Max'})
            Fmin = df2.groupby(['循环号']).min()
            Fmin = Fmin.reset_index()
            Fmin = Fmin.rename(columns={'F': 'F_Min'})
            Ffinal = pd.merge(Fmax, Fmin, on='循环号')
            Ffinal = pd.merge(Ffinal, dfcap, on='循环号')
            writer = pd.ExcelWriter(
                r'C:\Users\zhengyu.tang\Desktop\膨胀力数据处理例子\内部数据处理脚本\output\{}_PZL.xlsx'.format(name[:-5]))
            Ffinal.to_excel(writer, sheet_name='PZL', index=False)
            if a_list[len(a_list) - 1] > 50:
                for k in range(50, len(a_list) + 1, 50):
                    PZL2 = PZL1.loc[PZL1['循环号'] == k]
                    PZL2.to_excel(writer, sheet_name='{}'.format(k), index=None)
            writer.save()

