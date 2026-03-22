#!/bin/bash
# Start the backend server
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR/backend"

# Activate virtual environment
source venv/bin/activate

# Start uvicorn
echo "🚀 Starting NexusIntel Backend on http://localhost:8000"
echo "📄 API Docs: http://localhost:8000/docs"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
