#!/bin/bash

# Ensure a GitHub URL was provided
if [ -z "$1" ]; then
    echo "Error: You must provide a GitHub repository URL."
    echo "Usage: ./publish_to_github.sh <repository-url>"
    echo "Example: ./publish_to_github.sh https://github.com/username/repository.git"
    exit 1
fi

REPO_URL=$1

echo "Initializing Git repository..."
git init

echo "Adding files to repository..."
git add .

echo "Committing files..."
git commit -m "Initial commit including new files"

echo "Setting main branch..."
git branch -M main

echo "Adding remote repository: $REPO_URL"
git remote add origin "$REPO_URL"

echo "Pushing to GitHub..."
git push -u origin main

echo "Done! Your repository has been published."
