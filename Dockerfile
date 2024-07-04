FROM python:3.11-alpine

WORKDIR /app

ADD src ./src
ADD .env .
ADD requirements.txt .
ADD config.toml .

RUN python3 -m pip install -r requirements.txt

CMD [ "python3", "src/app.py" ]