FROM python:3.6-buster
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary
EXPOSE 5000
ENV STATIC_URL /static
ENV STATIC_PATH /static
ENV STATIC_INDEX 0
COPY swagger.json swagger.json
COPY . .
CMD ["flask", "run"]

