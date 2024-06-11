FROM python:3.12-slim

ENV PYTHONUNBUFFERED=0


WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src src
COPY run.sh run.sh

RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get clean && \
    chmod +x run.sh

CMD ["python" "run.py"]