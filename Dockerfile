# Playwright base image with Chromium
FROM mcr.microsoft.com/playwright/python:v1.49.0

WORKDIR /app

# Ensure Python prints immediately
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# Install Xvfb for virtual display
RUN apt-get update && apt-get install -y xvfb

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run Gunicorn wrapped with xvfb-run
CMD ["xvfb-run", "-a", "gunicorn", "-b", "0.0.0.0:6288", "--timeout", "180", "--capture-output", "--log-level", "debug", "app:app"]
