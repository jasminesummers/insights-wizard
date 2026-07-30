#!/bin/bash
# 🧙‍♂️ Insights Wizard — Automated Git Push Tool
# Usage:
#   ./push_to_github.sh "Optional custom commit message"

# Change to the directory containing this script
cd "$(dirname "$0")"

echo "🔍 Checking repository status..."

# Ensure we are tracking the git branch correctly
git branch -M main

# Add all modified & untracked files (excluding .gitignore entries)
git add .

# Check if there are changes to commit
if ! git diff-index --quiet HEAD --; then
    echo "📦 Packaging latest updates..."
    
    # Use custom message if passed as argument, otherwise use default
    if [ -n "$1" ]; then
        COMMIT_MSG="$1"
    else
        COMMIT_MSG="Update Insights Wizard: User Profiles & Sharing - $(date '+%Y-%m-%d %H:%M:%S')"
    fi
    
    git commit -m "$COMMIT_MSG"
    echo "✅ Changes committed successfully."
else
    echo "✨ No new changes detected to commit. Checking push status..."
fi

# Push to GitHub
echo "🚀 Pushing to https://github.com/jasminesummers/insights-wizard..."
git push origin main

if [ $? -eq 0 ]; then
    echo "🎉 Success! The latest code is live."
    echo "🌐 View it shortly at: https://jasminesummers.github.io/insights-wizard/"
else
    echo "❌ Push failed. Please check your GitHub credentials/token in your terminal."
fi
