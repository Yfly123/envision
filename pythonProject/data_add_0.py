import pandas as pd
import os


def add_zero():
    num_str = ''
    addr = r'C:\Users\fei.yang4\Documents\work\add 0'
    file_name = r'TVC报表验证数据对照组清单_20210719A.xlsx'

    os.chdir(addr)
    data = pd.read_excel(file_name, sheet_name='Sheet2')
    df = pd.DataFrame(data)
    temp = df[num_str]
    temp = temp.tolist()
    for i in range(len(temp)):
        if list(str(temp[i]))[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            temp[i] = '0' + str(temp[i])

    new_data = pd.DataFrame(temp)
    print(df.columns.values)
    df[num_str] = new_data
    new_file_name = "new_{}".format(file_name)
    df.to_excel(new_file_name, index=False)
if __name__ == '__main__':
    add_zero()
    print('运行结束！')
