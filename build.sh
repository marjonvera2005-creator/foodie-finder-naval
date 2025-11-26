#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create media directories BEFORE collectstatic
mkdir -p media/dishes
mkdir -p media/restaurants
mkdir -p media/restaurants/gallery
mkdir -p media/about

# Create sample images to persist
echo "Creating sample images..."
mkdir -p static/sample_images

# Create placeholder images using base64 data
echo 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==' | base64 -d > static/sample_images/placeholder.png

# Copy sample images to media
cp -r static/sample_images/* media/ 2>/dev/null || true

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Set permissions
chmod -R 755 media/ static/ staticfiles/ 2>/dev/null || true

echo "Build completed - media files preserved!"