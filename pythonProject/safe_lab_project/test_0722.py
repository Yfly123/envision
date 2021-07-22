"""
@Time ： 2021/7/22 15:52
@Auth ： Fei.Yang
"""
import datetime

file_addr=r'C:\Users\fei.yang4\Documents\work\safety_lab\input\stress_sensor_data\11-2020.csv'
import pandas as pd
data1 = pd.read_csv(file_addr)
data2 =pd.DataFrame(data1)
data2['Ch5'] = data2['Ch5'].apply(int)
res = data2.iloc[288097:291599,1:]

print(res['Ch5'])
print(res.dtypes)
# res.astype('int')
# print(type(res.iloc[0,1]))
# print(res)
# res['sum']=res.apply(lambda x:sum(x),axis=1)
# print(res)
