#!/usr/bin/env bash
os=$(uname)

echo "OS System: $os"
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
docker-compose up airflow-init

# Startup all the containers at once
docker-compose up -d
