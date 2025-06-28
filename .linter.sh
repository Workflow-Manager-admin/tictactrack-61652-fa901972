#!/bin/bash
cd /home/kavia/workspace/cmbc18fc77/tictactrack-61652-fa901972/tic_tac_toe_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

