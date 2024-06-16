#!/bin/bash


export PATH=$PATH:$HOME/smart_projector/server_proj/projview
FILE_PATH=$HOME/smart_projector
#echo "$PATH"

cd "$FILE_PATH" || exit

VENV_PATH="venv/bin/activate"

# Check if the virtual environment exists
if [ -f "$VENV_PATH" ]; then
    echo "Activating the virtual environment..."
    source "$VENV_PATH"
else
    echo "Virtual environment not found. Skipping activation."
fi

python3 main.py -l $DISPLAY
echo "Exiting current session..."
exit 0