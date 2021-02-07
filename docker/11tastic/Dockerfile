FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim as compile-image

WORKDIR /app
RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --user -r /app/requirements.txt; rm -r /tmp 
COPY ./app /app/app
