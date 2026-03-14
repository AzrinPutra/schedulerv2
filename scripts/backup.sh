#!/bin/bash
# Git backup script for FireSchedule

echo "Starting git backup..."
git add .
git commit -m "schedule update: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
echo "Backup completed!"
