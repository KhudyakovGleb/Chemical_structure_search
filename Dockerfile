FROM python:3.12-alpine3.20

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

ENTRYPOINT [ "fastapi", "run" ]
