#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create media directories BEFORE collectstatic
mkdir -p media/dishes
mkdir -p media/restaurants
mkdir -p media/restaurants/gallery
mkdir -p media/about

# Copy existing media files to static
cp -r media/* static/ 2>/dev/null || true

# Collect static files (includes media)
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Set permissions
chmod -R 755 media/ static/ staticfiles/ 2>/dev/null || true

echo "Build completed - media files preserved!"