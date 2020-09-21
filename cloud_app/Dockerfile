FROM python:3
RUN mkdir /data
WORKDIR /data
ADD requirements.txt /data
RUN pip3 install -r requirements.txt
ADD . /data
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
