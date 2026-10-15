FROM apache/spark:4.1.1-java21-python3

USER root

RUN wget -P /opt/spark/jars \
    -q https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.10/postgresql-42.7.10.jar

WORKDIR /home/app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

WORKDIR /opt/spark/work-dir

CMD ["python3", "/home/app/app.py"]