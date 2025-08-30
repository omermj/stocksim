FROM python:3.10.16-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Entrypoint waits for DB and preps the app
RUN chmod +x /app/entrypoint.sh

# Expose internal port
EXPOSE 8000

# app:app === {module}:{flask_instance}
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]