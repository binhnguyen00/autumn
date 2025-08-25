#!/bin/bash

ENV_DIR=$(pwd)/runtime/env.sh

source $ENV_DIR

function show_helps() {
  echo """
Usage: ./backend.sh <command>

Available commands:
  start   Start the backend
  debug   Debug the backend
  stop    Stop the backend
  """
}

function activate_venv() {
  source $PROJECT_DIR/$VENV_NAME/bin/activate
}

COMMAND=$1;
if [ -n "$COMMAND" ]; then
  shift
else
  echo "No command provided. Showing helps..."
  show_helps
  exit 1
fi

if [ "$COMMAND" = "start" ]; then
  cd $PROJECT_DIR
  activate_venv
  uvicorn \
    src.backend.app.Main:app \
    --host 0.0.0.0 \
    --port 8080 \
    --log-level info \
    --log-config $PROJECT_DIR/src/backend/logs/config.ini \
    --reload
elif [ "$COMMAND" = "debug" ]; then
  cd $PROJECT_DIR
  activate_venv
  python -m debugpy --listen 0.0.0.0:5678 -m uvicorn \
    src.backend.app.Main:app \
    --host 0.0.0.0 \
    --port 8080 \
    --log-level info \
    --log-config $PROJECT_DIR/src/backend/logs/config.ini \
    --reload
elif [ "$COMMAND" = "stop" ]; then
  # stop backend
  exit 0
else
  echo "Unknown command: $COMMAND"
  show_helps
  exit 1
fi