#!/bin/bash
set -e

echo "🚀 Starting BrowserPilot on Hugging Face Spaces..."

# Create outputs directory if it doesn't exist
mkdir -p /app/outputs

# Install dependencies if needed
if [ -f requirements.txt ]; then
    echo "📦 Installing Python dependencies..."
    pip install -q --no-cache-dir -r requirements.txt
fi

# Check if GOOGLE_API_KEY is set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "⚠️ WARNING: GOOGLE_API_KEY is not set!"
    echo "Please add it in Settings → Variables and secrets"
fi

# Check if DATABASE_URL is set (optional)
if [ -n "$DATABASE_URL" ]; then
    echo "✅ Database configured"
else
    echo "ℹ️ DATABASE_URL not set - database features disabled"
fi

# Start the application
echo "🌐 Starting FastAPI server on port 8000..."
exec python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
