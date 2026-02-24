#!/bin/bash
# Health check script for Docker setup

echo "=== Docker Infrastructure Health Check ==="
echo

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    exit 1
fi
echo "✅ Docker is running"

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found"
    exit 1
fi
echo "✅ docker-compose.yml exists"

# Validate docker-compose configuration
if docker compose config > /dev/null 2>&1; then
    echo "✅ Docker Compose configuration is valid"
else
    echo "❌ Docker Compose configuration has errors"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found (this is OK for testing)"
    echo "   Run 'make setup' or 'cp .env.example .env' to create it"
else
    echo "✅ .env file exists"
    
    # Check if GEMINI_API_KEY is set
    if grep -q "GEMINI_API_KEY=your_gemini_api_key_here" .env 2>/dev/null; then
        echo "⚠️  GEMINI_API_KEY is still set to placeholder value"
        echo "   Please update it with your actual API key"
    elif grep -q "GEMINI_API_KEY=" .env 2>/dev/null; then
        echo "✅ GEMINI_API_KEY is configured"
    fi
fi

# Check if required files exist
echo
echo "=== File Structure Check ==="
required_files=(
    "Dockerfile"
    "requirements.txt"
    "agents/main.py"
    "agents/__init__.py"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file is missing"
    fi
done

# Check if directories exist
required_dirs=(
    "agents"
    "data"
    "logs"
)

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir/ directory exists"
    else
        echo "❌ $dir/ directory is missing"
    fi
done

echo
echo "=== Health Check Complete ==="
