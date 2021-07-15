import os
import time
import numpy as np
import pylightxl
import xlrd
import openpyxl
import pandas as pd
from openpyxl import Workbook
class Sheet_operation():
    def __init__(self):
        #存放路径
        self.dir_path=[r'C:\Users\fei.yang4\Desktop\test']#\\10.202.16.10\tvc\03_Testing\10_TestingRecord\Projects-NonConfidential\09_Summary
    def get_files_dir(self):
        self.file_dir=[]
        for dirpath, dirnames, filenames in os.walk(self.dir_path[0]):
            for filename in filenames:
                new_dir=os.path.join(dirpath,filename)
                self.file_dir.append(new_dir)
        #将该目录下所有的子文件夹中的文件的路径保存在字符串数组中
        return self.file_dir
    #清洗路径
    def select_file(self):
        self.new_file_dirs=[]
        #提取文件路径中含有’测试申请单‘的路径
        self.file_dirs=self.get_files_dir()
        for dir in self.file_dirs:
            if '测试申' in dir :
                self.new_file_dirs.append(dir)
            else: continue
        return self.new_file_dirs
    #对每个含有'测试申请‘字样的xls文件进行提取数据'
    def operate_xls(self):
        self.file_dirs=self.select_file()
        for xls_dir in self.file_dirs:

            #由于每个excel中表单的名字不全为'测试申请单'，因此，先提取含有’样品申请单‘关键词表单的名字
            db=pylightxl.readxl(fn=xls_dir)
            sheets=pd.ExcelFile(xls_dir)
            # print(sheets.sheet_names)
            with open('test-0707.xlsx','a',encoding='utf-8') as f1:
                for sheet_name in sheets.sheet_names:
                    if "测试申请单" in sheet_name:
                        #将获取的表单名传入，进一步处理获取数据
                        ssd=db.ws(ws=sheet_name).ssd(keycols='样品生产编号',keyrows='样品生产编号')
                        # print(len(ssd[0]['keyrows']))
                        # print(ssd[0]['keyrows'])#样品生产编号
                        self.production_num=ssd[0]['keyrows']
                        self.index_col=ssd[0]['keycols']
                        self.index_col.insert(0,'样品生产编号')
                        self.val=ssd[0]['data']
                        # self.production_num=pd.Series(data=self.production_num)
                        # self.production_num.T
                        self.index_col=pd.Series(data=self.index_col)
                        self.val=pd.Series(data=self.val)
                        for i in range(len(self.production_num)):
                            f1.write(self.production_num)

                            print(self.production_num)
                    # print(self.production_num)

                    # for i in range(len(self.production_num)):
                    # val=pd.DataFrame(data=[self.production_num,self.val])
                    # print(val)



    def data_process(self,):
        pass

    # 输入参数为excel表格所在目录
    def to_one_excel(self):
        temp=pd.DataFrame()
        temp.to_excel('')
    def run(self):
        self.operate_xls()
s=Sheet_operation()
s.run()


