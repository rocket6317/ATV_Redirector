FROM mcr.microsoft.com/playwright/python:v1.49.0-focal

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 6288
CMD ["python", "app.py"]
