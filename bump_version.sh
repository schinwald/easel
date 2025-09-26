#!/bin/bash

# Bump version script for easel project
# Usage: ./bump_version.sh <patch|minor|major>

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <patch|minor|major>"
    exit 1
fi

VERSION_TYPE=$1

# Validate version type
if [[ ! "$VERSION_TYPE" =~ ^(patch|minor|major)$ ]]; then
    echo "Error: Version type must be patch, minor, or major"
    exit 1
fi

# Run bump-my-version using uv
uv run bump-my-version bump $VERSION_TYPE

echo "Version bumped to $(uv run bump-my-version show)"
