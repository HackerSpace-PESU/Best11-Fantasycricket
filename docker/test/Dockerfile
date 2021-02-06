FROM python:3

WORKDIR /test

COPY ./requirements.txt /test/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt; rm -r /tmp 
RUN pip install --no-cache-dir pytest;

COPY ./test /test/test
COPY ./app /test/app

CMD ["pytest"]

