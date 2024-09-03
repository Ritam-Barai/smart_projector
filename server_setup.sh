#!/bin/bash


#source "/home/pi/smart_projector/wm_script.sh"
echo "$IP_ADDR"
VENV_PATH="/home/pi/smart_projector/env/bin/activate"
if [ -f "$VENV_PATH" ]; then
    echo "Activating the virtual environment..."
    source "$VENV_PATH"
else
    echo "Virtual environment not found. Skipping activation."
fi
echo "$FILE_PATH"
cd "$FILE_PATH" || exit
DJANGO_URL="http://$IP_ADDR:8000"
echo "display: $DISPLAY"
if $DISPLAY &>/dev/null; then
  export DISPLAY=$DISPLAY
else
  export DISPLAY=:0
fi

python3 manage.py runserver "$IP_ADDR:8000"
sleep 1

