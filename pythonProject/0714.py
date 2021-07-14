import os
import time

import numpy as np
import pandas as pd
import openpyxl


class Sheet_set():
    def __init__(self):
        self.work_dir = r'C:\Users\fei.yang4\Documents\0713-lyy\申请单信息'  # 指定文件目录
        self.excel_dirs = []  # 所有excel的路径
        self.sheets_name = []

    # 将当前py的工作地址改为文件所在的地址
    def dir_set(self, ):
        os.chdir(path=self.work_dir)
        return os.getcwd()

    # 查找所有的excel的文件路径
    def fin_excel_dir(self):
        file_dir = self.dir_set()
        for dirpath, dirnames, filenames in os.walk(top=file_dir):
            for file_name in filenames:
                if file_name.endswith('.xlsx') or file_name.endswith('xls') or file_name.endswith('xlsm'):
                    new_dir = os.path.join(self.dir_set(), file_name)
                    self.excel_dirs.append(new_dir)

    # 获取每个excel中的sheets名字
    def get_sheets_name_from_excel(self, exc_dir):

        exc_file = pd.ExcelFile(exc_dir)
        sheets_name = exc_file.sheet_names
        return sheets_name

    # 提取excel里面的数据
    def operate_excel(self):
        i = 1  # 记录提取excel的进度
        all_data = pd.DataFrame()
        set_index = ['订单号', '测试编号', '样品编号', '测试项目细节', '收样日期', '测试项目', 'Vmax(V)', 'Vmin(V)', '容量(Ah)', '备注']
        for file in self.excel_dirs[3:4]:
            df1 = pd.DataFrame()
            j = 1  # 记录提取sheet的进度
            sheeets_name = self.get_sheets_name_from_excel(file)
            # 对每个sheet的数据进行读取
            for single_sheet in sheeets_name:
                print("共%s个excel，正在提取第%s个excel,此excel共%s个sheet,提取第%s个......" % (
                len(self.excel_dirs), i, len(sheeets_name), j))
                data = pd.read_excel(file, sheet_name=single_sheet)
                df = pd.DataFrame(data)
                columes = df.columns.values
                print(columes)
                print(single_sheet)

                if '订单号' and '测试编号' not in columes:  # 如果该sheet中索引无该项，则认为
                    continue
                try:
                    get_number = df['订单号'].values
                except:
                    get_number = df['测试编号'].values
                # 样品编号
                sample_number = df['样品编号'].values

                # 收样日期
                get_sample_data = df['收样日期'].values
                # 提取测试项目
                csxm = df['测试项目'].values
                # 提取测试项目细节
                if "项目细节" in columes:
                    s = [s for s in columes if '项目细节' in columes]
                    csxmxj = df[s[0]].values
                else:
                    csxmxj = pd.Series(len(sample_number) * [np.nan])
                    csxmxj=csxmxj.T
                # 提取Vmax(V)
                Vmax = df['Vmax(V)'].values
                # 提取Vmin(V)
                Vmin = df['Vmin(V)'].values
                # 提取容量(Ah)
                capacity = df['容量(Ah)'].values
                if "备注" in columes:
                    remark = df['备注'].values
                else:
                    remark = pd.Series(len(sample_number) * [np.nan])
                    remark = remark.T
                    print(len(remark))
                print(remark)
                total_data = np.hstack((get_number,sample_number,csxm,csxmxj,get_sample_data,Vmax,Vmin,capacity,remark))
                print(total_data)


                j += 1
                df1=np.vstack((total_data))


            i += 1
            # all_data为一个excel的所有sheeet 数据的汇总
            all_data = np.vstack((df1))

        # 由于数据过多可能会有问题
        total_data = pd.DataFrame(all_data, index=set_index)
        return total_data

    # 保存
    def save_to_excel(self):
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), '..')))
        try:  # 如果该文件不存在，则创建
            os.mkdir('results')
        except:
            print('results文件已存在，无需创建！')
        new_dir = os.path.join(os.getcwd(), 'results')
        # 更改绝对路路径
        os.chdir(new_dir)
        # 已将路径更改到results下，文件直接可以保存
        total_data = self.operate_excel()
        print("开始保存......")
        start_time = time.time()
        total_data.to_excel('电性能测试资源使用计划表_汇总-test.xlsx')
        print("保存完毕!用时%.2f" % (time.time() - start_time))

    def run(self):
        self.fin_excel_dir()
        self.save_to_excel()


if __name__ == '__main__':
    s_time = time.time()
    s = Sheet_set()
    s.run()
    print('总用时%.2f' % (time.time() - s_time))