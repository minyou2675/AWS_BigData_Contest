FROM python

WORKDIR /flask_app
ADD requirements.txt /flask_app/requirements.txt

#StatReloader에서 멈추는 문제 해결용 환경변수
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get -y update

RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
RUN pip install flask
RUN pip install gunicorn
RUN pip install pandas
RUN pip install boto3

