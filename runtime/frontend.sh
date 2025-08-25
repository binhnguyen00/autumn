#!/bin/bash

ENV_DIR=$(pwd)/runtime/env.sh

source $ENV_DIR

function show_helps() {
  echo """
Usage: ./frontend.sh <command>

Available commands:
  start   Start the frontend
  stop    Stop the frontend
  """
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
  cd $PROJECT_DIR/src/frontend
  pnpm run dev
elif [ "$COMMAND" = "stop" ]; then
  exit 0
else
  echo "Unknown command: $COMMAND"
  show_helps
  exit 1
fi