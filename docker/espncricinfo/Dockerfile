FROM python:3

WORKDIR /crawler

RUN pip install --no-cache-dir scrapyrt; rm -r /tmp 

COPY ./espncricinfo /crawler/espncricinfo
COPY ./scrapy.cfg /crawler/scrapy.cfg

EXPOSE 9080
CMD ["scrapyrt", "-i", "0.0.0.0"]

