FROM ubuntu
LABEL AUTHOR="Dotan Alter"
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENV FLASK_APP=tracking.py
CMD flask run --host=0.0.0.0