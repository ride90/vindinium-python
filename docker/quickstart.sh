#!/bin/bash
# Quick start script for local Vindinium server

set -e

echo "=========================================="
echo "Vindinium Local Server - Quick Start"
echo "=========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    echo ""
    echo "Please start Docker Desktop and try again."
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Start the server
echo "Starting Vindinium server..."
docker-compose up -d

echo ""
echo "Waiting for server to start..."
sleep 3

# Check if server is running
if docker-compose ps | grep -q "vindinium.*Up"; then
    echo ""
    echo "=========================================="
    echo "✅ Server is running!"
    echo "=========================================="
    echo ""
    echo "🌐 Open your browser: http://localhost"
    echo ""
    echo "Next steps:"
    echo "  1. Register an account at http://localhost"
    echo "  2. Create a bot and copy your API key"
    echo "  3. Edit ../.env and set:"
    echo "     SERVER=http://localhost"
    echo "     KEY=<your-api-key>"
    echo "  4. Run your bot: cd .. && python main.py"
    echo ""
    echo "Server management:"
    echo "  • View logs:  docker-compose logs -f vindinium"
    echo "  • Stop:       docker-compose down"
    echo "  • Restart:    docker-compose restart"
    echo ""
    echo "For full documentation, see: ../docs/LOCAL_SERVER.md"
    echo "=========================================="
else
    echo ""
    echo "❌ Error: Server failed to start"
    echo ""
    echo "Check logs with: docker-compose logs"
    exit 1
fi

