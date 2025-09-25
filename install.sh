#!/bin/bash

# Script to install the latest easel release from GitHub

REPO="schinwald/easel"
INSTALL_PATH="/usr/local/bin/easel"

# Detect OS
OS=$(uname -s)
case $OS in
    Linux)
        ASSET_NAME="main-linux"
        ;;
    Darwin)
        ASSET_NAME="main-macos"
        ;;
    *)
        echo "Unsupported OS: $OS"
        exit 1
        ;;
esac

# Get latest release asset URL
API_URL="https://api.github.com/repos/$REPO/releases/latest"
ASSET_URL=$(curl -s $API_URL | grep -A 5 "\"name\": \"$ASSET_NAME\"" | grep "browser_download_url" | sed 's/.*"browser_download_url": "\([^"]*\)".*/\1/')

if [ -z "$ASSET_URL" ]; then
    echo "Error: Could not find asset $ASSET_NAME in latest release."
    exit 1
fi

echo "Downloading easel from $ASSET_URL..."
curl -L -o /tmp/easel $ASSET_URL

echo "Installing easel to $INSTALL_PATH..."
sudo mkdir -p /usr/local/bin
sudo mv /tmp/easel "$INSTALL_PATH"
sudo chmod +x "$INSTALL_PATH"

echo "Installation complete! Run 'easel' to use the tool."
