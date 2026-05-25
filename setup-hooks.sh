#!/bin/bash

# Setup script for team members to install shared Git hooks (Linux/macOS version)

echo "Setting up Git hooks for this repository ..."

# Configure Git to use the shared hooks directory
git config core.hooksPath .githooks

echo ""
echo "Git hooks configured successfully!"
echo "The post-commit hook will now automatically update version.txt"
echo ""