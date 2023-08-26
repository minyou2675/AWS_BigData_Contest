import os
import fnmatch
import pandas as pd
import csv
import geopandas as gpd

root_path = os.getcwd() + '\yumin\의료,교육,상업,복지'
df = pd.DataFrame()
encodings = ['cp949', 'utf8', 'utf16', 'euckr']


#utf-8로 인코딩 안 된 엑셀파일은 일일이 utf-8 csv로 바꿔야 하는건가???

os.makedirs(os.getcwd()+'\yumin'+'\충청남도',exist_ok=True)
folder_list = [name for name in os.listdir(root_path)]

for folder in os.listdir(root_path):
    print("folder:",folder)
    for file in os.listdir(root_path+'\\'+folder):
        
        if fnmatch.fnmatch(file,'*충청남도*.csv'):
            print("file:",file)
            file_path = root_path+'\\'+folder+'\\'+file

            f = open(file_path,encoding='utf8')
            reader = csv.reader(f)
            csv_list = []
            for i in reader:
                csv_list.append(i)
            f.close()
            new_df = pd.DataFrame(csv_list)
            # new_df = pd.read_excel(root_path+'\\'+folder+'\\'+file,engine='openpyxl')
            df = pd.concat([df,new_df])
            print(df)



print(folder_list)


    