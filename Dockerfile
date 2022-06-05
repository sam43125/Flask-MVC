FROM python:3.9
COPY . /sample_crawler
WORKDIR /sample_crawler
EXPOSE 8080/tcp
EXPOSE 8080/udp
RUN pip install -r ./requirements.txt
CMD ["python", "runserver.py"]