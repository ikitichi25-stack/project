#!/bin/bash
set -e

echo "Starting SecureShop services..."
docker compose up -d

echo "Running OWASP ZAP baseline scan against http://127.0.0.1:8080"
docker run --rm --network host owasp/zap2docker-stable zap-baseline.py -t http://127.0.0.1:8080 -r zap-report.html

echo "Stopping services..."
docker compose down
