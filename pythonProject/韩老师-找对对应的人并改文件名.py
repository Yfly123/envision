#该程序为识别多个EXCEL文件名中对应的生产编号，并从总文件中找到对应生产编号的人，最后把人名加到对应的excel名前面
import pandas as pd
import os
import re
class Get_name():
    def __init__(self):
        self.dic1={}
        self.addr=r'C:\Users\fei.yang4\Documents\work\han\test'
        self.name_addr=r'C:\Users\fei.yang4\Documents\work\han\数据分配.xlsx'
        self.excel_addr=[]
        self.bianhao = []
        self.filenames=[]
        self.name=[]
        self.new_bianhao=[]
    def get_excel_name(self):
        for dirpath, dirnames, filenames in os.walk(top=self.addr):
            for file_name in filenames:
                if file_name.endswith('.xlsx') or file_name.endswith('xls') or file_name.endswith('xlsm'):
                    new_dir = os.path.join(self.addr,file_name)
                    self.filenames.append(file_name)
                    self.excel_addr.append(new_dir)
                    self.bianhao.append(re.findall(r'T2\d+C?',new_dir))

    def get_data1(self):
        addr_num = dict(zip(self.excel_addr,self.bianhao))
        data = pd.read_excel(self.name_addr,sheet_name='Sheet2')
        df = pd.DataFrame(data)
        for name in df.columns:
            for bh in self.bianhao:
                for temp in df[name].values:
                    if bh:
                        if str(bh[0]) in str(temp):
                            self.new_bianhao.append(str(bh[0]))
                            self.name.append(str(name))
        self.dic1 = dict(zip(self.new_bianhao,self.name))

    def change_name(self):
        self.get_excel_name()
        self.get_data1()
        print(self.dic1)
        for dirpath, dirnames, filenames in os.walk(top=self.addr):
            for file_name in filenames:
                if file_name.endswith('.xlsx') or file_name.endswith('xls') or file_name.endswith('xlsm'):
                    new_dir = os.path.join(self.addr,file_name)

                    temp = re.findall(r'T2\d+C?',new_dir)

                    if temp:
                        temp=str(temp[0])

                        try:
                            os.rename(new_dir,self.dic1[temp]+os.path.basename(new_dir))
                        except:
                            print(new_dir)

    def run(self):
        self.change_name()
        print(len(self.filenames))

if __name__=='__main__':
    g = Get_name()
    g.run()