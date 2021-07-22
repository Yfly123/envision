import os
import time
import numpy as np
import pandas as pd
class Sheet_set():
    def __init__(self):
        # 指定文件目录
        self.work_dir=r"C:\Users\fei.yang4\Desktop\results\jixing\3"
        self.sheets_name=[]
        self.file_dir = []
        self.erro_file_addr = []

    # 将当前py的工作地址改为文件所在的地址
    def dir_set(self):
        os.chdir(path=self.work_dir)
        return os.getcwd()

    # 查找所有的excel的文件路径
    def fin_excel_dir(self):

        for dirpath, dirnames, filenames in os.walk(self.work_dir):
            for file_name in filenames:
                if '存储' in file_name or '放电' in file_name:
                    continue
                if file_name.endswith('.xlsx') or file_name.endswith('xls') or file_name.endswith('xlsm'):

                    new_dir = os.path.join(dirpath, file_name)
                    self.file_dir.append(new_dir)
        # 将该目录下所有的子文件夹中的文件的路径保存在字符串数组中

    #获取每个excel中的sheets名字
    def get_sheets_name_from_excel(self,exc_dir):
        exc_file=pd.ExcelFile(exc_dir)
        sheets_name=exc_file.sheet_names
        return sheets_name

    #提取excel里面的数据
    def operate_excel(self):
        i=1#记录提取excel的进度
        df2=pd.DataFrame()
        set_index=['测试申请单号','测试编号','生产编号','电压(v)','内阻（mΩ)','记录人','日期', '备注']

        for file in self.file_dir:
            df1 = pd.DataFrame()
            j=1#记录提取sheet的进度
            sheeets_name=self.get_sheets_name_from_excel(file)
            #对每个sheet的数据进行读取
            for single_sheet in sheeets_name:
                print("共%s个excel，正在提取第%s个excel,此excel共%s个sheet,提取第%s个......"%(len(self.file_dir),i,len(sheeets_name),j))
                # 文件头所在的行

                for file_header in [5,6,7]:
                    data=pd.read_excel(file,sheet_name=single_sheet,header=file_header)
                    df = pd.DataFrame(data)
                    columes=df.columns.values
                    if "生产编号" not in columes:
                        continue
                    else:
                        # try:
                        #     #新表
                        #     try:
                        #         all_data=data.iloc[:,[1,2,3,4,5,13,14,15,16]]
                        #     except:
                        #         all_data=data.iloc[:,[1,2,3,4,5,11,12,13,14]]
                        # except:
                        #     #老表
                        #     try:
                        #         all_data = data.iloc[:, [1,2,3,4,5,12,13,14,15,16]]
                        #     except:
                        #         all_data = data.iloc[:, [1, 2, 3, 4, 5, 12, 13, 14]]
                        #3月之后的
                        try:
                            all_data = data.iloc[:, [1, 2, 3, 4, 5, 14, 15, 16,17]]
                        except:
                            try:
                                all_data = data.iloc[:, [1, 2, 3, 4, 5, 13,14, 15, 16]]
                            except:
                                all_data = data.iloc[:, [1, 2, 3, 4, 5, 11, 12, 13, 14]]

                        all_data=all_data.drop_duplicates()
                    j += 1
                df1 = pd.concat([all_data, df1],axis=0)
            i+=1
            df2 = pd.concat([df2, df1],axis=0)

        return df2

    #保存
    def save_to_excel(self):
        # os.chdir(os.path.abspath(os.path.join(os.getcwd(),'..')))
        # try:#如果该文件不存在，则创建
        #     os.mkdir('results')
        # except:
        #     print('results文件已存在，无需创建！')
        # new_dir=os.path.join(os.getcwd(),'results')
        # #更改绝对路路径
        # os.chdir(new_dir)
        #已将路径更改到results下，文件直接可以保存
        total_data=self.operate_excel()
        print("开始保存......")
        start_time=time.time()
        # erro_file=pd.DataFrame(self.file_without_get)
        # erro_file.to_excel('no_process_sheet.xlsx')
        total_data.to_excel('汇总-2021-3之后.xlsx',index=False)
        print("保存完毕!用时%.2f"%(time.time()-start_time))
    def run(self):
        self.fin_excel_dir()
        self.save_to_excel()

if __name__ =='__main__':
    s_time=time.time()
    s=Sheet_set()
    s.run()
    print('总用时%.2f'%(time.time()-s_time))