#!/bin/bash
# Start the frontend dev server
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR/frontend"

echo "🌐 Starting NexusIntel Frontend on http://localhost:3000"
npx vite --host 0.0.0.0 --port 3000
