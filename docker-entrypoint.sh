#!/bin/sh

# Starting logger service
echo "Starting logger service"
uvicorn src.main:app --port 8181 --workers 3
