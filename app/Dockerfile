FROM python:3.12

WORKDIR /app/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["sh", "-c", "
    python init_db.py &&
    uvicorn main:app --host 0.0.0.0 --port 8000
"]