# Use the official Playwright base image (includes Chromium, codecs, and dependencies)
FROM mcr.microsoft.com/playwright/python:v1.49.0-focal

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (served via Gunicorn)
CMD ["gunicorn", "-b", "0.0.0.0:6288", "app:app"]
