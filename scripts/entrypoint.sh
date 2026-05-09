#!/bin/bash
set -e

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-blogdb}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-postgres}"

echo ">>> Esperando a PostgreSQL en ${DB_HOST}:${DB_PORT}..."

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -q; do
    echo "    PostgreSQL no disponible — reintentando en 2s..."
    sleep 2
done

echo ">>> PostgreSQL disponible. Inicializando esquema..."

PGPASSWORD="$DB_PASSWORD" psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -c "
        CREATE TABLE IF NOT EXISTS articles (
            id         SERIAL       PRIMARY KEY,
            title      VARCHAR(200) NOT NULL,
            content    TEXT         NOT NULL,
            created_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
        );
    "

echo ">>> Esquema listo. Iniciando API..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
