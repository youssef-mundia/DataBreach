#!/bin/bash

# DataBreach Monitor - Development Setup Script

echo "🛡️  DataBreach Monitor - Development Setup"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backend/logs
mkdir -p frontend/build
mkdir -p docker/data

# Copy environment file
if [ ! -f backend/.env ]; then
    echo "📝 Creating environment file..."
    cp backend/.env.example backend/.env
    echo "✅ Environment file created. Please edit backend/.env with your settings."
fi

# Build and start services
echo "🏗️  Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🔍 Checking service health..."
docker-compose ps

# Run database migrations (if any)
echo "🔄 Running database setup..."
docker-compose exec backend python -c "
import asyncio
from app.core.database import init_db
asyncio.run(init_db())
print('Database initialized successfully')
"

echo ""
echo "🎉 Setup completed!"
echo ""
echo "🌐 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🔑 Default login credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "📊 Database connections:"
echo "   PostgreSQL: localhost:5432"
echo "   Redis: localhost:6379"
echo ""
echo "🛠️  To stop services: docker-compose down"
echo "🗂️  To view logs: docker-compose logs -f [service_name]"