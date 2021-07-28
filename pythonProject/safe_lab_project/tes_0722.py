# """
# @Time ： 2021/7/22 15:52
# @Auth ： Fei.Yang
# """
import re

import pandas as pd
import numpy as np
#
# file_addr=r'C:\Users\fei.yang4\Documents\work\safety_lab\input\stress_sensor_data\11-2020.csv'
# import pandas as pd
# data1 = pd.read_csv(file_addr,low_memory=False)
# data1=data1.iloc[:,1:]
# data2 =pd.DataFrame(data1)
# res = data2.iloc[288097:291599,:].astype(float)
# res['sum']=res.apply(lambda x:sum(x),axis=1)
# res = res.sort_values(by='sum')
# result = res.iloc[[-1],:]
# print(result)
# print(type(result))
# # print(res['Ch5'])
# # print(res.dtypes)
#
#
#
# # res.astype('int')
# # print(type(res.iloc[0,1]))
# # print(res)
# # res['sum']=res.apply(lambda x:sum(x),axis=1)
# # print(res)
te=[1,2,3,2,3,2,]
list(set(te))
print(te)
