FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    xvfb \
    chromium \
    libavcodec-extra \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and Chromium
RUN pip install playwright && playwright install chromium

WORKDIR /app
COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:6288", "app:app"]
