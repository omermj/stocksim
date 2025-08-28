FROM python:3.10.16-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose internal port
EXPOSE 8000

# app:app === {module}:{flask_instance}
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]