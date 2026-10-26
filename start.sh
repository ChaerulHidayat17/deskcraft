#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
echo "Starting DeskCraft Portal on http://0.0.0.0:8000 ..."
exec uvicorn app:app --host 0.0.0.0 --port 8000 --reload
