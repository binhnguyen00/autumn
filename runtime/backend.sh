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
  echo "Activating virtual environment..."
  source $PROJECT_DIR/$VENV_NAME/bin/activate
}

function prepare_whisper_model() {
  echo "Preparing whisper model..."
  if [ -d "$WHISPER_MODEL_DIR" ] && [ "$(find "$WHISPER_MODEL_DIR" -mindepth 1 -maxdepth 1 -type d | head -n 1)" ]; then
    echo "Found whisper model"
  else
    python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='mobiuslabsgmbh/faster-whisper-large-v3-turbo')"
  fi
}

function start() {
  activate_venv
  prepare_whisper_model
  cd $PROJECT_DIR

  echo "Starting..."
  uvicorn \
    src.backend.app.Main:app \
    --host 0.0.0.0 \
    --port 8080 \
    --log-level info \
    --reload
}

function debug() {
  activate_venv
  prepare_whisper_model
  cd $PROJECT_DIR

  echo "Debugging..."
  python -m debugpy --listen 0.0.0.0:5678 -m uvicorn \
    src.backend.app.Main:app \
    --host 0.0.0.0 \
    --port 8080 \
    --log-level info \
    --reload
}

function stop() {
  # TODO: Implement
  exit 0
}

# ============================
# controller
# ============================

COMMAND=$1;
if [ -n "$COMMAND" ]; then
  shift
else
  echo "No command provided. Showing helps..."
  show_helps
  exit 1
fi

if [ "$COMMAND" = "start" ]; then
  start
elif [ "$COMMAND" = "debug" ]; then
  debug
elif [ "$COMMAND" = "stop" ]; then
  stop
else
  echo "Unknown command: $COMMAND"
  show_helps
  exit 1
fi