import os
import time
import pandas as pd
class Sheet_set():
    def __init__(self):
        # 指定文件目录
        self.work_dir=r'\\10.202.16.10\tvc\03_Testing\10_TestingRecord\Lab1&Lab2\1_ACR&OCV及极性特性记录表\ACR&OCV\7.14'
        self.excel_dirs=[]#所有excel的路径
        self.sheets_name=[]
        self.file_without_get=[]

    # 将当前py的工作地址改为文件所在的地址
    def dir_set(self,):
        os.chdir(path=self.work_dir)
        return os.getcwd()

    # 查找所有的excel的文件路径
    def fin_excel_dir(self):
        file_dir=self.dir_set()
        for dirpath, dirnames, filenames in os.walk(top=file_dir):
            for file_name in filenames:
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
        set_index=['内部编码' '生产编号' 'OCV/V' 'ACR/mΩ' '测试人员' '测试日期' '备注']
        for file in self.excel_dirs:
            df1=pd.DataFrame()
            j=1#记录提取sheet的进度
            sheeets_name=self.get_sheets_name_from_excel(file)
            #对每个sheet的数据进行读取
            for single_sheet in sheeets_name:
                print("共%s个excel，正在提取第%s个excel,此excel共%s个sheet,提取第%s个......"%(len(self.excel_dirs),i,len(sheeets_name),j))
                # 文件头所在的行
                file_header=4
                data=pd.read_excel(file,sheet_name=single_sheet,header=file_header)
                df = pd.DataFrame(data)
                columes=df.columns.values
                if len(columes)==0:
                    self.file_without_get.append([file,single_sheet])
                    continue
                else:
                    #'内部编码' '生产编号' 'OCV/V' 'ACR/mΩ' '测试人员' '测试日期' '备注'
                    nbbm = df["内部编码"]
                    scbh = df["生产编号"]
                    ocv = df["OCV/V"]
                    acr = df["ACR/mΩ"]
                    t_name = df['测试人员']
                    t_date = df["测试日期"]
                    bz = df["备注"]
                    total_data=pd.concat([nbbm,scbh,ocv,acr,t_name,t_date,bz],axis=1)
                    # total_data.columns=set_index
                    total_data=total_data.drop_duplicates()#删除每行相同的数据
                j += 1
                df1=pd.concat([df1,total_data],axis=0)
            i += 1
            #all_data为一个excel的所有sheeet 数据的汇总
            all_data = pd.concat([all_data, df1])
        return all_data

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
        self.save_to_excel()

if __name__ =='__main__':
    s_time=time.time()
    s=Sheet_set()
    s.run()
    print('总用时%.2f'%(time.time()-s_time))