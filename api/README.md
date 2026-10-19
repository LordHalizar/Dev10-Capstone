# Flask API w/ Spark

## Steps

1. YAML

    ```yaml
    api:
        build: ./api
        restart: always
        container_name: api
        hostname: api
        ports:
        - 5000:5000 # Spark API
        volumes:
        - ./conf:/opt/spark/conf
        - ./work-dir:/opt/spark/work-dir
        - ./output:/opt/spark/files/out
        - ./input:/opt/spark/files/in
        networks:
        - spark-network
    ```

2. Dockerfile

3. Convert an image to Apache Spark 4.*.

4. Execute `python3 /home/app/app.py`.