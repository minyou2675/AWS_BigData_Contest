from flask import Flask, render_template
import pandas as pd
import os
import boto3
import io
import json
app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/')
def map(): 
    return render_template('map.html')

@app.route('/map/<int:param>/')
def info(param):
    s3_client = boto3.client(service_name="s3",
                         aws_access_key_id="AKIAZFEQRMP3352X2BXB",
                         aws_secret_access_key="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")

    obj = s3_client.get_object(Bucket="farmfarmtal", Key="new_infra.csv")
    obj2 = s3_client.get_object(Bucket="farmfarmtal", Key="population.csv")
    df = pd.read_csv(io.BytesIO(obj["Body"].read())) 
    df2 = pd.read_csv(io.BytesIO(obj2["Body"].read())) 
    
    # 지원사업 크롤링
    file_path = './static/crawling.json'
    crawling_dict = {}
    with open(file_path,'r') as file:
        crawling_dict = json.load(file)
    print(crawling_dict)
    
    # df = pd.read_csv('./static/new_infra.csv')
    # df2 = pd.read_csv('./static/population.csv')
    
    #모든 컬럼에 대한 평균 값 
    column_means = {}
    for column_name in df.columns:
        if '정보' in column_name:
            mean_value = df[column_name].mean()
            column_means[column_name] = mean_value
    
    row = df.loc[param]
    emd_nm = row['EMD_NM']
    sgg_nm = row['SGG_NM']
    hos_cnt = row['의료']
    com_cnt = row['상업']
    well_cnt = row['복지']
    edu_cnt = row['교육']
    
    #순위
    hospital_rank = int(row['의료순위'])
    commercial_rank = int(row['상업순위'])
    wellfare_rank = int(row['복지순위'])
    education_rank = int(row['교육순위'])
    infra_rank = int(df2.loc[df2['SGG_NM'] == sgg_nm ]['infra_rank'])
    emd_total = len(df)
    average_rank = int((((hospital_rank+commercial_rank+wellfare_rank+education_rank)/4)*100)/emd_total)

    #특이사항 기능
    speciality = {}
    speciality_cnt = {}
    for column_name in df.columns:  
        if '정보' in column_name and row[column_name] >= column_means[column_name]:
            speciality[column_name[0:-2]] = True
            speciality_cnt[column_name[0:-2]] = row[column_name]
        else:
            speciality[column_name[0:-2]] = False
            speciality_cnt[column_name[0:-2]] = row[column_name]
    print(speciality)
    
    params = {
        'average_rank' : average_rank, 'crawling_dict' : crawling_dict,
        'speciality' : speciality, 'speciality_cnt' : speciality_cnt,
        'infra_rank' : infra_rank,
        'hospital_rank' : hospital_rank, 'commercial_rank':commercial_rank,'wellfare_rank':wellfare_rank,'education_rank':education_rank,
        'emd_total':emd_total,'sgg_nm' : sgg_nm, 'emd_nm' : emd_nm, 
        'hospital' : hos_cnt, 'commercial' : com_cnt, 'wellfare' : well_cnt, 'education' : edu_cnt}
    #병원 수 , ~중에 몇 등
    #지원 정보 
    return render_template('info.html',param=params)
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='5000')
