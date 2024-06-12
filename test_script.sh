#!/bin/bash

# Check if IP address argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <ip_address>"
    exit 1
fi

IP_ADDRESS=$1
TEMP_DIR=$(mktemp -d)  # Create a temporary directory

echo "Created temporary directory: $TEMP_DIR"

# Change directory to the temporary directory
cd "$TEMP_DIR" || exit 1

# Python script execution
python3  --ipaddress "$IP_ADDRESS"

# Clean up: Delete the temporary directory
cd ~  # Return to home directory
rm -rf "$TEMP_DIR"

echo "Deleted temporary directory: $TEMP_DIR"
