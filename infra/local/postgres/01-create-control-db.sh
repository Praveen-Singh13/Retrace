#!/bin/bash
set -Eeuo pipefail

: "${POSTGRES_MIGRATOR_PASSWORD:=local-only}"
psql \
  --username "$POSTGRES_USER" \
  --dbname "$POSTGRES_DB" \
  --set=migrator_password="$POSTGRES_MIGRATOR_PASSWORD" \
  --set=ON_ERROR_STOP=1 \
  --file=/docker-entrypoint-initdb.d/01-create-control-db.sql.in
