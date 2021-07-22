import re

import openpyxl
from openpyxl import Workbook
import pandas as pd
addr1 = r'C:\Users\fei.yang4\Documents\work\lyy找到对应人\报表样本07.xlsx'
addr2 = r'C:\Users\fei.yang4\Documents\work\lyy找到对应人\数据分配07.xlsx'
def search_data():
    data = pd.read_excel(addr2,sheet_name='Sheet2')
    df =pd.DataFrame(data)
    for name in df.columns:
        df.apply(lambda x:re.search(r'T2\d+C?',df[name]),axis=1)
        print(df[re.search(r'T2\d+C?',df[name])])
        print(df[str(name)])


def data_fill():

    data = pd.ExcelFile(addr1)
    sheets_names = data.sheet_names
    for sheet_na in sheets_names:

        data = pd.read_excel(addr1,sheet_name=sheet_na)
        df = pd.DataFrame(data)
        sq_num = df['申请单号'].tolist()
        print(sq_num)

if __name__ =='__main__':
    search_data()