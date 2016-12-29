FROM python:3.5

MAINTAINER Han Wang <goodwanghan@gmail.com>

WORKDIR /code 

COPY requirements.txt /code/

RUN pip3 install -r requirements.txt 

COPY run-2.py /code/ 

COPY fin /code/fin 

ENTRYPOINT ["python","/code/run-2.py"]

