FROM python:3.12-slim

ENV PYTHONUNBUFFERED=0

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src src
COPY run.py run.py

RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get clean

CMD ["python", "run.py"]
