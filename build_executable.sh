#!/bin/bash

# Script to build a single executable for the easel project

echo "Syncing dependencies..."
uv sync

echo "Building executable with PyInstaller..."
uv run pyinstaller --onefile main.py

echo "Build complete! Executable is in dist/main"
