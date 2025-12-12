# Official Playwright base image with Chromium + codecs
FROM mcr.microsoft.com/playwright/python:v1.49.0

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run Flask app via Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:6288", "app:app"]
