FROM python:3.8.3-slim-buster
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN pip3 install Flask
COPY /src /app
WORKDIR /app
CMD ["python3", "Server.py"]
