FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install flask && \ 
    pip install requests 

EXPOSE 5000

CMD ["python", "/app/app.py"]
