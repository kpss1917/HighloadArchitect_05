FROM python:3.10

WORKDIR /app

RUN pip3 install psycopg2

COPY . .

EXPOSE 8000

#CMD [ "python3", "httpServer.py" ]
ENTRYPOINT [“python3”, "httpServer.py”]