#!/bin/bash
set -e

echo "Running Checkov IaC scan on docker-compose.yml"
checkov -f docker-compose.yml
