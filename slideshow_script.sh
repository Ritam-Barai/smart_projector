#!/bin/bash


export PATH=$PATH:$HOME/smart_projector/server_proj/projview
FILE_PATH=$HOME/smart_projector
#echo "$PATH"

cd "$FILE_PATH" || exit

python3 main.py -l $DISPLAY
echo "Exiting current session..."
exit 0