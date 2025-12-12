FROM python:3.10-slim

# Install system dependencies required by Playwright Chromium
RUN apt-get update && apt-get install -y \
    curl wget gnupg libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libgbm1 libasound2 libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m playwright install chromium

# Copy app code
COPY . /app
WORKDIR /app

CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
