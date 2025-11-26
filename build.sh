#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create media directories
mkdir -p media/dishes
mkdir -p media/restaurants
mkdir -p media/restaurants/gallery
mkdir -p media/about

# Set permissions for media directory
chmod -R 755 media/

echo "Build completed successfully!"