FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install playwright \
    && playwright install chromium

COPY app.py .

EXPOSE 6288

CMD ["python", "app.py"]
