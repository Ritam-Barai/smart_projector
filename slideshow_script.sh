#!/bin/bash


export PATH=$PATH:/home/pi/smart_projector/server_proj/projview
FILE_PATH=/home/pi/smart_projector
#echo "$PATH"

cd "$FILE_PATH" || exit

VENV_PATH="env/bin/activate"

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
