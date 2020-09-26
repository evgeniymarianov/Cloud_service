FROM python:3
RUN mkdir /data
WORKDIR /data
ADD requirements.txt /data
RUN pip3 install -r requirements.txt
ADD . /data
CMD python3 ./manage.py makemigrations \
  && python3 ./manage.py migrate \
  && python3 ./manage.py runserver 0.0.0.0:8000
