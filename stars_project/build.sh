#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

echo "Starting build process..."

# Set environment variables for build
export DJANGO_SETTINGS_MODULE=stars.settings
export BUILD_PHASE=true

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Debug information
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -la

# Check if manage.py exists
if [ ! -f "manage.py" ]; then
    echo "Error: manage.py not found in current directory"
    exit 1
fi

# Test Django setup
echo "Testing Django setup..."
python manage.py check --deploy

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run migrations
echo "Running database migrations..."
python manage.py migrate

echo "Build completed successfully!"
