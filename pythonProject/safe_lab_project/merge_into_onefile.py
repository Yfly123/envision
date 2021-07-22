"""
@Time ： 2021/7/22 13:15
@Auth ： Fei.Yang
"""
import os
import pandas as pd
class file_operation():
    def __init__(self):
        #压力数据文件所在的上级目录
        self.file_addr = r'C:\Users\fei.yang4\Documents\work\safety_lab\成功数据处理实例\成功数据处理实例\02膨胀力原始数据及数据文件合并\数据采集仪上拷贝传感器原始数据test'
        os.chdir(self.file_addr)
    def merge_to_one(self):
        temp_data=pd.DataFrame()
        for dirpath, dirnames, filenames in os.walk(self.file_addr):
            for file_name in filenames:
                if file_name.endswith('.csv'):
                    new_file_addr=os.path.join(dirpath,file_name)
                    temp_d = pd.read_csv(new_file_addr)
                    df = pd.DataFrame(temp_d)
                    temp_data = pd.concat([temp_data,df])
        temp_data.sort_values(by='Datetime')
        return temp_data
    def save_tofile(self):
        print('开始保存......')
        res_data = self.merge_to_one()
        #最终保存的csv文件可能太大，建议将merge_result.csv后缀改为txt打开
        res_data.to_csv('merge_result.csv',index=False)
        print('保存结束......')
if __name__=='__main__':
    fo = file_operation()
    fo.save_tofile()
