import pandas as pd
data  = pd.ExcelFile(r'C:\Users\fei.yang4\Documents\work\han\汤钲宇T21040061C——DCPR data.xlsx')
sheets_names = data.sheet_names
df1=pd.DataFrame()
for sheet_na in sheets_names:
    df = pd.read_excel(data,sheet_name=sheet_na)
    new_data=df.iloc[:,1]
    new_data=list(new_data)
    for i in range(len(new_data)):
        if list(str(new_data[i]))[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            new_data[i] = '0' + str(new_data[i])
    scbh = pd.DataFrame(new_data)
    df1= pd.concat([df1,scbh])
df1.to_excel('result1.xlsx')