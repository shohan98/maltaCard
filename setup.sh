#!/bin/bash

# MaltaCard Project Setup Script for macOS
# This script will automatically set up the entire development environment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if file exists
file_exists() {
    [ -f "$1" ]
}

# Function to check if directory exists
dir_exists() {
    [ -d "$1" ]
}

# Print welcome message
echo -e "${GREEN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                    MaltaCard Project Setup                   ║
║                                                              ║
║  This script will automatically set up your development     ║
║  environment for the MaltaCard project.                     ║
║                                                              ║
║  What this script will do:                                   ║
║  ✓ Check and install required tools                         ║
║  ✓ Create virtual environment                               ║
║  ✓ Install Python dependencies                              ║
║  ✓ Set up environment variables                             ║
║  ✓ Run database migrations                                  ║
║  ✓ Create superuser (optional)                             ║
║  ✓ Start the development server                             ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS only!"
    exit 1
fi

print_status "Starting MaltaCard project setup..."

# Check if Homebrew is installed
print_status "Checking Homebrew installation..."
if ! command_exists brew; then
    print_warning "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for this session
    eval "$(/opt/homebrew/bin/brew shellenv)"
    print_success "Homebrew installed successfully!"
else
    print_success "Homebrew is already installed!"
fi

# Check and install Python 3.13
print_status "Checking Python 3.13 installation..."
if ! command_exists python3.13; then
    print_warning "Python 3.13 not found. Installing Python 3.13..."
    brew install python@3.13
    print_success "Python 3.13 installed successfully!"
else
    print_success "Python 3.13 is already installed!"
fi

# Check and install Git
print_status "Checking Git installation..."
if ! command_exists git; then
    print_warning "Git not found. Installing Git..."
    brew install git
    print_success "Git installed successfully!"
else
    print_success "Git is already installed!"
fi

# Check and install Docker (optional)
print_status "Checking Docker installation..."
if ! command_exists docker; then
    print_warning "Docker not found. Would you like to install Docker? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_status "Installing Docker Desktop..."
        brew install --cask docker
        print_success "Docker Desktop installed successfully!"
        print_warning "Please start Docker Desktop manually after installation."
    else
        print_warning "Docker installation skipped. You can install it later if needed."
    fi
else
    print_success "Docker is already installed!"
fi

# Check if we're in the project directory
if ! file_exists "manage.py"; then
    print_error "This script must be run from the MaltaCard project root directory!"
    print_error "Please navigate to the project directory and run this script again."
    exit 1
fi

print_success "Project directory confirmed!"

# Create virtual environment if it doesn't exist
print_status "Checking virtual environment..."
if ! dir_exists ".venv"; then
    print_warning "Virtual environment not found. Creating .venv..."
    python3.13 -m venv .venv
    print_success "Virtual environment created successfully!"
else
    print_success "Virtual environment already exists!"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source .venv/bin/activate
print_success "Virtual environment activated!"

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip
print_success "Pip upgraded successfully!"

# Install Python dependencies
print_status "Installing Python dependencies..."
if file_exists "requirements.txt"; then
    pip install -r requirements.txt
    print_success "Python dependencies installed successfully!"
else
    print_error "requirements.txt not found!"
    exit 1
fi

# Create .env file if it doesn't exist
print_status "Checking environment configuration..."
if ! file_exists ".env"; then
    print_warning ".env file not found. Creating .env file..."
    
    # Generate a secure secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
    
    cat > .env << EOF
# Django Settings
DEBUG=True
SECRET_KEY=${SECRET_KEY}
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DATABASE_URL=sqlite:///db.sqlite3

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=shohan.plan@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=shohan.plan@gmail.com

# Google OAuth Settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-google-oauth2-key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-google-oauth2-secret

# Security Settings
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
EOF
    
    print_success ".env file created successfully!"
    print_warning "Please update the .env file with your actual email and OAuth credentials!"
else
    print_success ".env file already exists!"
fi

# Create logs directory
print_status "Creating logs directory..."
mkdir -p logs
print_success "Logs directory created!"

# Create static directory
print_status "Creating static directory..."
mkdir -p static
print_success "Static directory created!"

# Run database migrations
print_status "Running database migrations..."
python manage.py migrate
print_success "Database migrations completed successfully!"

# Create superuser (optional)
print_status "Would you like to create a superuser? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    print_status "Creating superuser..."
    python manage.py createsuperuser
    print_success "Superuser created successfully!"
else
    print_warning "Superuser creation skipped. You can create one later with: python manage.py createsuperuser"
fi

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput
print_success "Static files collected successfully!"

# Test the setup
print_status "Testing the setup..."
python manage.py check
print_success "Django setup is valid!"

# Show available commands
echo -e "${GREEN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                    Setup Complete! 🎉                        ║
║                                                              ║
║  Your MaltaCard development environment is ready!            ║
║                                                              ║
║  Available commands:                                         ║
║  • python manage.py runserver    - Start development server ║
║  • python manage.py shell        - Open Django shell        ║
║  • python manage.py createsuperuser - Create admin user     ║
║  • python manage.py test         - Run tests                ║
║  • docker-compose up -d         - Start with Docker        ║
║                                                              ║
║  Access URLs:                                                ║
║  • http://localhost:8000/       - Main application         ║
║  • http://localhost:8000/admin/ - Django admin             ║
║  • http://localhost:8000/swagger/ - API documentation      ║
║  • http://localhost:8000/api/   - API endpoints            ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Ask if user wants to start the server
print_status "Would you like to start the development server now? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    print_status "Starting development server..."
    print_status "Server will be available at: http://localhost:8000/"
    print_status "Press Ctrl+C to stop the server"
    echo ""
    python manage.py runserver
else
    print_status "To start the server later, run: python manage.py runserver"
fi

print_success "Setup completed successfully! 🚀" 