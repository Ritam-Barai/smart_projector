#!/bin/bash

PIDS=$(lsof -ti:8000 )
:<<'COMMENT'
cleanup() {
    echo "Cleaning up before exit..."
    # Perform any cleanup here
    exit 0
}
COMMENT

# Trap SIGINT and SIGTERM signals and call the cleanup function
trap cleanup SIGINT SIGTERM
# Check if PID is not empty
for PID in $PIDS; do
    echo "PID: $PID"
    if [ ! -z "$PID" ] && ps -p $PID -o comm= | grep -iq python; then
    # Kill the process
    kill -SIGTERM $PID
    echo "Server on port 8000 has been stopped."
    else
    echo "No python process is running on port 8000."
    fi
done  
