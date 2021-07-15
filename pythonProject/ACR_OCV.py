import os
import time
import numpy as np
import pylightxl
import xlrd
import openpyxl
import pandas as pd

class Sheet_operation():
    def __init__(self):
        #存放路径
        self.dir_path=[r'C:\Users\fei.yang4\Desktop\极性']

    def get_files_dir(self):
        self.file_dir=[]
        self.erro_file_addr=[]
        for dirpath, dirnames, filenames in os.walk(self.dir_path[0]):
            for filename in filenames:
                new_dir=os.path.join(dirpath,filename)
                self.file_dir.append(new_dir)
        #将该目录下所有的子文件夹中的文件的路径保存在字符串数组中
        return self.file_dir

    #清洗路径
    def select_file(self):
        # self.new_file_dirs=[]
        self.file_dirs=self.get_files_dir()
        for dir in self.file_dirs:
            if '极性' not in dir:
                self.file_dirs.remove(dir)
        return self.file_dirs

    #对每个含有'测试申请‘字样的xls文件进行提取数据'
    def operate_xls(self):
        self.file_dirs=self.select_file()
        i=1
        j=0
        df1=pd.DataFrame()
        for xls_dir in self.file_dirs:
            print(xls_dir)
            print('复制第%s个文件，还剩%s个文件,错误文件为%s'%(i,len(self.file_dirs)-i,j))
            i += 1
            try:
                xlrd_book=xlrd.open_workbook(xls_dir)
                data=pd.read_excel(xlrd_book,sheet_name=0)
                df=pd.DataFrame(data)
                df1=pd.concat([df,df1])
            except:
                self.erro_file_addr.append(xls_dir)
                j+=1
        print('开始保存...')
        df1.to_excel('acr_ocv_all_3.xlsx')
        df2=pd.DataFrame(self.erro_file_addr)
        df2.to_excel('erro_file_acr.xlsx')

    # 输入参数为excel表格所在目录
    def to_one_excel(self):
        temp=pd.DataFrame()
        temp.to_excel('')
    def run(self):
        print(len(self.select_file()))
        self.operate_xls()

if __name__=='__main__':
    start_time=time.time()
    s=Sheet_operation()
    s.run()
    endtime=time.time()
    print('运行结束！,总耗时%s'%(endtime-start_time))
