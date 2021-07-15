import os
import time
import numpy as np
import pandas as pd
import openpyxl
class Sheet_set():
    def __init__(self):
        # 指定文件目录
        self.work_dir=r"C:\Users\fei.yang4\Desktop\results\jixing"
        self.excel_dirs=[]#所有excel的路径
        self.sheets_name=[]
        self.file_without_get=[]

    # 将当前py的工作地址改为文件所在的地址
    def dir_set(self):
        os.chdir(path=self.work_dir)
        return os.getcwd()

    # 查找所有的excel的文件路径
    def fin_excel_dir(self):
        file_dir=self.dir_set()
        for dirpath, dirnames, filenames in os.walk(top=file_dir):
            for file_name in filenames:
                if '存储' in file_name or '放电' in file_name:
                    continue
                if file_name.endswith('.xlsx') or file_name.endswith('xls') or file_name.endswith('xlsm'):
                    new_dir = os.path.join(self.dir_set(),file_name)
                    self.excel_dirs.append(new_dir)

    #获取每个excel中的sheets名字
    def get_sheets_name_from_excel(self,exc_dir):
        exc_file=pd.ExcelFile(exc_dir)
        sheets_name=exc_file.sheet_names
        return sheets_name

    #提取excel里面的数据
    def operate_excel(self):
        i=1#记录提取excel的进度
        all_data=pd.DataFrame()
        set_index=['测试申请单号','测试编号','生产编号','电压(v)','内阻（mΩ)','记录人','日期', '备注']

        for file in self.excel_dirs:
            df1=pd.DataFrame()
            j=1#记录提取sheet的进度
            sheeets_name=self.get_sheets_name_from_excel(file)
            #对每个sheet的数据进行读取
            for single_sheet in sheeets_name:
                print("共%s个excel，正在提取第%s个excel,此excel共%s个sheet,提取第%s个......"%(len(self.excel_dirs),i,len(sheeets_name),j))
                # 文件头所在的行
                file_header=7 or 8
                data=pd.read_excel(file,sheet_name=single_sheet,header=file_header)
                df = pd.DataFrame(data)
                columes=df.columns.values
                print(columes)

    #保存
    def save_to_excel(self):
        os.chdir(os.path.abspath(os.path.join(os.getcwd(),'..')))
        try:#如果该文件不存在，则创建
            os.mkdir('results')
        except:
            print('results文件已存在，无需创建！')
        new_dir=os.path.join(os.getcwd(),'results')
        #更改绝对路路径
        os.chdir(new_dir)
        #已将路径更改到results下，文件直接可以保存
        total_data=self.operate_excel()
        print("开始保存......")
        start_time=time.time()
        erro_file=pd.DataFrame(self.file_without_get)
        erro_file.to_excel('no_process_sheet.xlsx')
        total_data.to_excel('ACR_OCV_汇总.xlsx')
        print("保存完毕!用时%.2f"%(time.time()-start_time))
    def run(self):
        self.fin_excel_dir()
        # self.save_to_excel()
        self.operate_excel()

if __name__ =='__main__':
    s_time=time.time()
    s=Sheet_set()
    s.run()
    print('总用时%.2f'%(time.time()-s_time))