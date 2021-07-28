"""
@Time ： 2021/7/26 22:16
@Auth ： Fei.Yang
"""
# coding:utf-8
import pandas as pd
import os,re,logging
import numpy as np
import datetime as dt
class Data_pro():
    def __init__(self):
        self.root_addr = r'C:\Users\fei.yang4\Documents\work\safety_lab'
        self.processed_time=''
        self.pre_data=pd.DataFrame()
        self.old_pre_addr=[]
        self.make_file_and_log()
        logging.basicConfig(level=logging.WARN,
                            filename='.\logs\log-' + dt.datetime.now().strftime('%Y-%m-%d') + '.txt', filemode='a',
                            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        # formate设置输出格式，年月日分秒毫秒，行数，等级名，打印的信息
        logging.info("logs_output文件夹创建成功！")
    #从特定表中特定sheet中找数据
    def choose_data(self,file_addr,sheet_na):
        data = pd.read_excel(file_addr,sheet_name=sheet_na)
        return data

    #将循环数据表和工步数据表按循环号对应起来，整合到一张表
    def inter_table(self):
        file_addr=self.root_addr+'\input\step_data'
        os.chdir(file_addr)
        res = pd.DataFrame()
        for dirpath, dirnames, filenames in os.walk(os.getcwd()):
            for file_name in filenames:
                file_addr = os.path.join(dirpath,file_name)
                cycle_data=self.choose_data(file_addr,'循环数据表')
                df1 = pd.DataFrame(cycle_data)
                new_cycle_data=df1[['循环序号', '放电容量(Ah)', '充电容量(Ah)']]
                step_data=self.choose_data(file_addr,"工步数据表")
                df2 = pd.DataFrame(step_data)
                new_step_data = df2[['循环号', '绝对时间']]
                # 将数据中按工步序号找到开始时间
                new_step_data = self.find_start_time(new_step_data)
                res_data = pd.concat([new_cycle_data,new_step_data],axis=1)
                res=pd.concat([res,res_data],axis=0)
        return res

    def find_start_time(self,step_data):
        start_data = step_data.groupby('循环号').first()
        start_data = start_data.values
        start_data = pd.DataFrame(start_data, columns=["起始时间"])
        return start_data

    def get_preesur_file(self,time1):
        sensor_data_addr = os.path.join(os.getcwd(), '..') + '\stress_sensor_data'
        os.chdir(sensor_data_addr)
        try:
            temp = re.findall(r'2\d{3}?', str(time1))
            for dirpath, dirnames, filenames in os.walk(sensor_data_addr):
                for file_name in filenames:
                    if file_name.endswith('.csv') and str(temp[0]) in file_name:
                        csv_addr = os.path.join(dirpath, file_name)
                        return csv_addr
        except:
            logging.warning(' %s在压力数据文件查询不到！'%time1)
    #根据所给时间在pressure数据文件中找到与该时间差最近的数据的索引
    def find_press_pos_of_step_num(self,time1):
        #找该时间所保存的压力数据所在的文件
        csv_addr = self.get_preesur_file(time1)
        addr_temp=csv_addr[-15:]
        # addr_temp=re.findall('2\d{3}',addr_temp)
        # time_temp = re.findall('2\d{3}',time1)

        if self.pre_data.empty or not self.old_pre_addr or self.old_pre_addr !=csv_addr:
            data1 = pd.read_csv(csv_addr,low_memory=False)
            self.pre_data=data1
            self.old_pre_addr=csv_addr

        data = [time1] * len(self.pre_data['Datetime'])
        data = pd.to_datetime(data)
        new_df = (pd.to_datetime(self.pre_data['Datetime']) - data)
        new_df = pd.to_timedelta(abs(new_df))

        min_data = new_df.min()
        min_data = pd.to_timedelta(min_data)
        pos = new_df[new_df == min_data].index.tolist()

        return pos[0],time1

    #输入数据为开始时间集,获取相邻时间戳直接传感器数据值
    def search_pressure_data(self, data_summary):
        pos_temp=[]
        temp = pd.DataFrame()
        temp_data=data_summary
        data_summary=data_summary.loc[:,['起始时间']]
        k,j=0,0
        for i in range(len(data_summary)):
            time_data=data_summary.iat[i,0]
            # print(time_data)
            try:
                pos,time1 = self.find_press_pos_of_step_num(str(time_data))
            except:
                continue
            pos_temp.append(pos)
            file_addr = self.get_preesur_file(time1)
            if len(pos_temp)>=2:
                data_res = pd.DataFrame(temp_data.iloc[[i - 1],[0,1,2]])
                data1 = pd.read_csv(file_addr, low_memory=False)
                data1 = data1.iloc[:, 1:]
                data2 = pd.DataFrame(data1)
                data2.replace('  ------ ',np.nan)
                data2.replace(np.nan,0)

                res = data2.iloc[pos_temp[0]:pos_temp[1], :]
                try:
                    res=res.astype(float)
                except:
                    res = res.replace('  ------ ', np.nan)
                    res = res.dropna(axis=0,how='all')
                    res = res.replace(np.nan, 0)
                    res=res.astype(float)
                res['sum'] = res.apply(lambda x: sum(x), axis=1)
                res = res.sort_values(by='sum')
                colum=data2.columns.tolist()
                new_index = colum+colum
                new_index.insert(len(colum),'Fmax')
                new_index.append('Fmin')
                new_index.insert(0, '放电容量(Ah)')
                new_index.insert(0,'充电容量(Ah)')
                new_index.insert(0,'循环序号')
                try:
                    result = res.iloc[[-1], :].values
                    result1= res.iloc[[0],:].values
                    new_data = np.hstack([data_res,result,result1])
                    new_data = pd.DataFrame(new_data,columns=new_index)
                    temp = pd.concat([temp,new_data])
                    j+=1
                except:
                    k +=1

                    logging.warning("%s时间段没有压力测试数据..."%time1[0])

                # print(temp)
                pos_temp.pop(0)
            print("已完成%s,跳过%s,还剩%s..."%(j,k,len(temp_data)-i))
        return temp

    #在文件里创建output文件以及log.txt
    def make_file_and_log(self):
        self.change_dir()
        try:
            os.mkdir('logs')
            os.mkdir('output')
        except:
            print('output文件存在，无需创建！')

    #更改路径
    def change_dir(self):
        try:
            os.chdir(self.root_addr)
        except:
            print('路径更改失败，检查文件路径')
            logging.error('路径更改失败，检查文件路径')
    def save_file_to_results(self,res):
        file_addr = self.root_addr + '\output'
        os.chdir(file_addr)
        res.to_csv('test-0727-new.csv',encoding='utf_8_sig',index=False)

    def run(self):
        step_and_start_time_data = self.inter_table()
        res = self.search_pressure_data(step_and_start_time_data)
        self.save_file_to_results(res)

if __name__=='__main__':
    dp = Data_pro()
    #1、将循环数据表和工步数据表进行整合
    dp.run()