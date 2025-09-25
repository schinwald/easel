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

# Construct latest release asset URL
ASSET_URL="https://github.com/$REPO/releases/latest/download/$ASSET_NAME"

echo "Downloading easel from $ASSET_URL..."
curl -L -o /tmp/easel $ASSET_URL

echo "Installing easel to $INSTALL_PATH..."
sudo mkdir -p /usr/local/bin
sudo mv /tmp/easel "$INSTALL_PATH"
sudo chmod +x "$INSTALL_PATH"

echo "Installation complete! Run 'easel' to use the tool."
