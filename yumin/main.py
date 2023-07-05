import requests
import xml.etree.ElementTree as ET
from os import name
import xml.etree.ElementTree as et
import pandas as pd
import bs4
from time import sleep
from urllib.parse import urlencode, quote_plus, unquote

#법정동 코드 수집
bgd = []
bgd_dict = {}
with open('./법정동코드 전체자료.txt','r') as file:
    lines = file.readlines()
    
for line in lines:
    bgd_temp = line.split('\t')
    bgd_exist = True if bgd_temp[-1].strip('\n') == '존재' else False
    if bgd_exist:
        bgd_temp[-1] = bgd_temp[-1].strip('\n')
        bgd.append(bgd_temp)

'''
결과코드	Result_Code	3	필수	200	결과코드
결과메세지	Result_Msg	50	필수	OK	결과메시지
한 페이지 레코드 수	Rcdcnt	10	필수	10	한 페이지당 표출 데이터 레코드 수
페이지 수	Page_No	10	필수	1	페이지 수
데이터 총 개수	Total_Count	15	필수	1	데이터 총 개수
결과 정렬 번호	No	10	필수	1	검색 결과 정렬 번호
법정동코드(동/리)	BJD_Code	10	필수	4215034022	요청 값 포함 일치하는 법정동코드에 대한 토양검정 화학성 목록 정보 검색
시료채취년도	Any_Year	4	필수	2019	토양검정 시료 채취년도 (YYYY)
토양검정일	Exam_Day	2	필수	20190101	토양검정일 (YYYYMMDD)
경지구분코드	Exam_Type	1	필수	1	경지구분 식별 ID 값 *경지구분 코드표 참조
대상지 지번주소	Pnu_Nm	100	필수	강원도 강릉시 강동면 모전리 5번지	지번주소
산도	ACID	10	필수	6.9	산도(pH)
유효인산	VLDPHA	10	필수	36.2	유효인산(mg/kg)
유효규산	VLDSIA	10	필수	72.1	유효규산(mg/kg)
유기물	OM	10	필수	13.2	유기물(g/kg)
마그네슘	POSIFERT_MG	10	필수	1.7	마그네슘(cmol+/kg)
칼륨	POSIFERT_K	10	필수	0.19	칼륨(cmol+/kg)
칼슘	POSIFERT_CA	10	필수	4.9	칼슘(cmol+/kg)
전기전도도	SELC	10	필수	0.29	전기전도도(dS/m)
'''


    
# for x in bgd:
#     url = 'http://apis.data.go.kr/1390802/SoilEnviron/SoilExam/getSoilExamList'
   
#     params ={'serviceKey' : 't8AvYGqeSITi2+gahkha6EK2mJWV35JR0ujirjhE08+zehJAVTDJeJDbocgW6CpEisnA85+U6H7gJqo9oCc1bA==', 'Page_Size' : 10 , 'Page_No' : 1, 'BJD_Code' : x[0] }
#     response = requests.get(url, params=params)
#     print(response.content)
#     bgd_dict[x[1]] = response.content

# print(bgd_dict)


url = 'http://apis.data.go.kr/1390802/SoilEnviron/SoilExam/getSoilExamList'
decoding_key = 't8AvYGqeSITi2+gahkha6EK2mJWV35JR0ujirjhE08+zehJAVTDJeJDbocgW6CpEisnA85+U6H7gJqo9oCc1bA=='
content = ''


for x in bgd:
    params ={'serviceKey' : decoding_key, 'Page_Size' : '10', 'Page_No' : '1', 'BJD_Code' : 	x[0] }
    response = requests.get(url, params=params,verify=False)
    content += response.text
    print(content)
    sleep(5)
    

xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
rows = xml_obj.find_all('item')
print(rows)

row_list = []
column_list = []
value_list = []

for i in range(0,len(rows)):
    columns = rows[i].find_all()
    for j in range(len(columns)):
        if i == 0:
           column_list.append(columns[j].name)
        value_list.append(columns[j].text)
    row_list.append(value_list)
    value_list = []

df = pd.DataFrame(row_list,columns=column_list)
print(df)






