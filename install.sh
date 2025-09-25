#!/bin/bash

# Script to install the easel executable

EXECUTABLE="dist/main"
INSTALL_PATH="/usr/local/bin/easel"

if [ ! -f "$EXECUTABLE" ]; then
    echo "Error: Executable not found at $EXECUTABLE. Run build_executable.sh first."
    exit 1
fi

echo "Installing easel to $INSTALL_PATH..."
sudo mkdir -p /usr/local/bin
sudo cp "$EXECUTABLE" "$INSTALL_PATH"
sudo chmod +x "$INSTALL_PATH"

echo "Installation complete! Run 'easel' to use the tool."
