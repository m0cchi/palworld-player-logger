FROM python:3.10

ADD . /usr/local/app
WORKDIR /usr/local/app

RUN pip install -r requirements.txt
RUN cd /usr/local/bin && curl -O https://raw.githubusercontent.com/m0cchi/wait_for_tcp/master/wait_for_tcp.py && chmod +x wait_for_tcp.py

CMD bash bootstrap.sh

