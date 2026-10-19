FROM apache/spark:4.1.1-java21-python3

USER root

WORKDIR /opt/spark/work-dir

RUN wget -P /opt/spark/jars \
    -q https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.10/postgresql-42.7.10.jar

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER 185