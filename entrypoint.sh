#!/usr/bin/env sh
set -e

# Wait for Postgres
if [ -n "$DATABASE_URL" ]; then
  echo "Waiting for database at $(echo "$DATABASE_URL" | sed -E 's/^.*:\/\/(.*)@/\1@/; s/@.*$//' )"
fi

host=$(echo "$DATABASE_URL" | sed -E 's/^.*@([^:]+):.*$/\1/')
port=$(echo "$DATABASE_URL" | sed -E 's/^.*:([0-9]+)\/.*$/\1/')

if [ -z "$host" ]; then
  host=db
fi
if [ -z "$port" ]; then
  port=5432
fi

echo "Waiting for Postgres at $host:$port..."
for i in $(seq 1 30); do
  if nc -z "$host" "$port" >/dev/null 2>&1; then
    echo "Postgres is up."
    break
  fi
  echo "...still waiting ($i)"
  sleep 1
done

# Optional: run simple DB init so SQLAlchemy can create tables if seed.py expects it
python - <<'PY'
from app import app
from db import db
with app.app_context():
    db.create_all()
print("DB ready")
PY

exec "$@"
