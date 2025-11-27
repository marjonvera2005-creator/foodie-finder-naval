#!/usr/bin/env python
"""
Test Cloudinary upload functionality
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodie_finder.settings')
django.setup()

import cloudinary.uploader
from django.core.files.base import ContentFile
from core.models import Restaurant, RestaurantImage

def test_cloudinary_upload():
    print("Testing Cloudinary upload...")
    
    # Test direct Cloudinary upload
    try:
        # Create a simple test image content
        test_content = b"Test image content"
        
        # Upload directly to Cloudinary
        result = cloudinary.uploader.upload(
            ContentFile(test_content),
            public_id="test_upload",
            folder="test"
        )
        
        print(f"Direct upload successful: {result['secure_url']}")
        
        # Clean up test image
        cloudinary.uploader.destroy(result['public_id'])
        print("Test image cleaned up")
        
        return True
        
    except Exception as e:
        print(f"Cloudinary upload failed: {str(e)}")
        return False

def check_configuration():
    print("Checking Cloudinary configuration...")
    
    config = cloudinary.config()
    print(f"Cloud Name: {config.cloud_name}")
    print(f"API Key: {config.api_key}")
    print(f"Secure: {config.secure}")
    
    from django.conf import settings
    print(f"Storage Backend: {settings.DEFAULT_FILE_STORAGE}")

if __name__ == '__main__':
    check_configuration()
    test_cloudinary_upload()