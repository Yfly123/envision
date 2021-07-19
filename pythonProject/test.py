import pandas as pd
import os
class File_process():

    def __init__(self):
        self.dianxin_num_addr=r"C:\Users\fei.yang4\Documents\work\0716_file_deal\存储电芯编号.xlsx"
        self.total_file=r"C:\Users\fei.yang4\Documents\work\0716_file_deal\极性记录表 (lyy3).xls"
        self.without_deal_num=[]
        self.deal_num=[]

    # 1、获取需要查询的电芯编号
    def get_dianxin_number(self):
        data = pd.read_excel(self.dianxin_num_addr)
        d_dx = pd.DataFrame(data)
        d_dx.sort_values()
        dx_num = d_dx["电芯编号"].to_list()
        return dx_num

   #对编号前面加0
    def add_fron_(self):
        data=pd.read_excel(self.dianxin_num_addr)
        df = pd.DataFrame(data)
        product_num = df["电芯编号"]
        product_num = product_num.tolist()
        for i in range(len(product_num)):
            if list(str(product_num[i]))[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                product_num[i] = '0' + str(product_num[i])
        product_num = pd.DataFrame(product_num)
        df["电芯编号"] = product_num
        return df

    # 3、根据电芯编号从文件获得数据(根据‘生产编号’对数据进行分块)
    def get_data_from_file(self):
        dx_num=self.get_dianxin_number()
        data = pd.read_excel(self.total_file)
        df = pd.DataFrame(data)
        t_date = df["日期 "]
        t_date = pd.to_datetime(t_date)
        df["日期 "] = t_date.apply((lambda x: x.date()))
        lst=[g for _,g in df.groupby("生产编号")]
        return lst

    #4、堆叠整合数据
    def summary_data(self):
        dx_num=self.get_dianxin_number()
        lst =self.get_data_from_file()
        # for cont in lst:


    #5、保存数据
    def save_to_excel(self):
        lst =self.get_data_from_file()
        dx_num=self.get_dianxin_number()
        print("开始保存...")
        i = 1
        os.chdir(os.path.join(self.total_file, '..'))
        try:  # 如果该文件不存在，则创建
            os.mkdir('results')
        except:
            print('results文件已存在，无需创建！')
        new_dir = os.path.join(os.getcwd(), 'results')
        os.chdir(new_dir)
        for part_data in lst:
            print("共%s,处理了%s..." % (len(dx_num), i))
            pro_num = part_data["生产编号"].values[0]
            if pro_num in dx_num:
                file_name = "{}.xlsx".format(pro_num)
                part_data.to_excel(file_name,index=False)
                i += 1
                self.deal_num.append(pro_num)
            else:
                continue
        d_num=pd.DataFrame(self.deal_num)
        d_num.to_excel('deal_num.xlsx',index=False)
if __name__ == "__main__":
    fp = File_process()
    # fp.get_dianxin_number()
    fp.save_to_excel()