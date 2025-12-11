FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y curl \
    && pip install --no-cache-dir -r requirements.txt \
    && playwright install chromium

COPY app.py .

EXPOSE 6288

CMD ["python", "app.py"]
