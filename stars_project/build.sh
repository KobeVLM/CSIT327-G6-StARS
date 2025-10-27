#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

echo "Starting build process..."

# Set environment variables for build
export DJANGO_SETTINGS_MODULE=stars.settings
export BUILD_PHASE=true

# Ensure we have a secret key for build
if [ -z "$SECRET_KEY" ]; then
    echo "Warning: No SECRET_KEY provided, using build-time fallback"
    export SECRET_KEY="build-time-key-for-collectstatic-only"
fi

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Debug information
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -la

# Check environment variables
echo "Environment variables during build:"
echo "DEBUG: $DEBUG"
echo "SECRET_KEY: ${SECRET_KEY:0:10}..." 
echo "ALLOWED_HOSTS: $ALLOWED_HOSTS"
echo "CLOUDINARY_URL: ${CLOUDINARY_URL:0:20}..."
echo "BUILD_PHASE: $BUILD_PHASE"
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"

# Check if manage.py exists
if [ ! -f "manage.py" ]; then
    echo "Error: manage.py not found in current directory"
    exit 1
fi

# Test Django installation and settings
echo "Testing Django installation..."
python -c "import django; print(f'Django version: {django.get_version()}')"
python -c "import os; print(f'Settings module: {os.environ.get(\"DJANGO_SETTINGS_MODULE\")}')"

# Test settings import
echo "Testing settings import..."
python -c "from django.conf import settings; print('Settings imported successfully')"

# Test Django setup (skip deployment checks during build)
echo "Testing basic Django setup..."
python manage.py check --settings=stars.settings

# Collect static files with explicit settings
echo "Collecting static files..."
python manage.py collectstatic --no-input --settings=stars.settings

# Run migrations with explicit settings
echo "Running database migrations..."
python manage.py migrate --settings=stars.settings

echo "Build completed successfully!"
