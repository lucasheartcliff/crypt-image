#!/usr/bin/env bash
set -e

WORKSPACE="${CODESPACE_VSCODE_FOLDER:-$(pwd)}"

echo "Starting backend..."
PYTHONPATH="$WORKSPACE" uvicorn backend.app.main:app \
  --host 0.0.0.0 --port 8000 --reload \
  > /tmp/backend.log 2>&1 &

echo "Starting frontend..."
cd "$WORKSPACE/frontend"
npm run dev > /tmp/frontend.log 2>&1 &

echo "Both services started."
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:8000/docs"
