FROM python:3.6

ADD . /code
RUN pip3 install git+https://github.com/nkoshell/flask-peewee-crud.git

EXPOSE 8000

WORKDIR /code

CMD ["python", "simple_server.py"]
