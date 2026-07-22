#!/bin/bash
# Configura o banco de dados PostgreSQL para o Sistema de Mudancas

set -e

DB_NAME="${DB_NAME:-mudancas}"
DB_USER="${DB_USER:-postgres}"

# Detecta se precisa de sudo para conectar como DB_USER
# (peer authentication exige que o usuario do OS coincida com o do PG)
if [ "$DB_USER" = "$(whoami)" ]; then
    PSQL="psql -U $DB_USER"
else
    PSQL="sudo -u $DB_USER psql"
fi

echo "=== Criando banco de dados $DB_NAME ==="
$PSQL -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || echo "Banco ja existe."

echo "=== Executando schema.sql ==="
$PSQL -d "$DB_NAME" -f schema.sql

echo "=== Executando triggers.sql ==="
$PSQL -d "$DB_NAME" -f triggers.sql

echo "=== Populando com seed.sql ==="
$PSQL -d "$DB_NAME" -f seed.sql

echo "=== Setup completo! ==="
echo "Para rodar a aplicacao:"
echo "  cd aplicacao && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python app.py"
