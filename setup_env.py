#!/usr/bin/env python3
"""
Helper script to generate a .env file for the MaltaCard Django project.
This script will create a .env file with proper default values.
"""

import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key

def generate_env_file():
    """Generate a .env file with proper default values."""
    
    # Check if .env already exists
    env_file = Path('.env')
    if env_file.exists():
        print("⚠️  .env file already exists. Skipping generation.")
        print("If you want to regenerate, delete the existing .env file first.")
        # return
    
    # Generate a new secret key
    secret_key = get_random_secret_key()
    
    # Create the .env content
    env_content = f"""# Django Settings
SECRET_KEY={secret_key}
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DATABASE_URL=sqlite:///db.sqlite3

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@maltacard.com

# Google OAuth Settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-google-oauth2-key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-google-oauth2-secret

# Security Settings
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
"""
    
    # Write the .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    print("📝 Please update the following values in your .env file:")
    print("   - EMAIL_HOST_USER: Your email address")
    print("   - EMAIL_HOST_PASSWORD: Your email app password")
    print("   - SOCIAL_AUTH_GOOGLE_OAUTH2_KEY: Your Google OAuth key")
    print("   - SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET: Your Google OAuth secret")
    print("\n🔒 Remember: Never commit your .env file to version control!")

if __name__ == '__main__':
    generate_env_file() 