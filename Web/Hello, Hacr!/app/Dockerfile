FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt && pip3 install flask_sqlalchemy && pip3 install markdown && pip3 install flask_WTF && pip3 install flask_talisman

COPY ./app/ .

EXPOSE 5000

CMD ["python", "app.py"]