FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

EXPOSE 8080

# COPY ./ /app

CMD ["python", "main.py"]
