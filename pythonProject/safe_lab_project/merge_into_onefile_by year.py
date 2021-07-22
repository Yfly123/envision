"""
@Time ： 2021/7/22 14:28
@Auth ： Fei.Yang
"""
import os
import re
import pandas as pd
class file_operation():
    def __init__(self):
        #压力数据文件所在的上级目录
        self.file_addr = r'C:\Users\fei.yang4\Documents\work\safety_lab\成功数据处理实例\成功数据处理实例\02膨胀力原始数据及数据文件合并\数据采集仪上拷贝传感器原始数据test'
        os.chdir(self.file_addr)
    def merge_to_one(self,year_data):
        temp_data=pd.DataFrame()
        for dirpath, dirnames, filenames in os.walk(self.file_addr):
            for file_name in filenames:
                if file_name.endswith('.csv') and str(year_data) in file_name:
                    new_file_addr=os.path.join(dirpath,file_name)
                    temp_d = pd.read_csv(new_file_addr)
                    df = pd.DataFrame(temp_d)
                    temp_data = pd.concat([temp_data,df])
        temp_data.sort_values(by='Datetime')
        return temp_data
    def get_file_year(self):
        contain_year = []
        for dirpath, dirnames, filenames in os.walk(self.file_addr):
            for file_name in filenames:
                if file_name.endswith('.csv'):
                    str_tem=re.findall(r'2\d{3}?',file_name)
                    contain_year.append(int(str_tem[0]))
                    contain_year=list(set(contain_year))
        return contain_year
    def save_tofile(self):#避免数据量过大，也便于后续查询，采用按年保存
        print('开始保存......')
        contain_year = self.get_file_year()
        i=0
        for y in contain_year:
            i+=1
            res_data = self.merge_to_one(y)
            #最终保存的csv文件可能太大，建议将merge_result.csv后缀改为txt打开
            print('保存了%d,还剩%d year'%(y,len(contain_year)-i))
            file_name='{}_result'.format(y)
            res_data.to_csv(file_name+'.csv',index=False)
        print('保存结束......')
if __name__=='__main__':
    fo = file_operation()
    fo.save_tofile()
