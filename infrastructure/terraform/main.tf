#  Interview Practice - Local Development Infrastructure
# main configuration containing actual resources to create.
# when I run terraform apply, it reads the resource definition, creates file with specified content 
# and tracks what it created in terraform.tfstate

terraform {
  required_version = ">= 1.0"
  required_providers {
    # Using local provider for demonstration
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

#  Local File Storage
resource "local_file" "interview_ai_config" {
  content = jsonencode({
    project_name = var.project_name
    environment  = var.environment
    storage_path = "./uploads"
    database_url = "sqlite:///./interview_ai.db"
    redis_url    = "redis://localhost:6379"
  })
  filename = "${path.module}/config.json"
}

#  Local Logging
resource "local_file" "interview_ai_logs" {
  content = "# Interview Practice Application Logs\n"
  filename = "${path.module}/logs/app.log"
}

#  Python Virtual Environment Setup Guide
resource "local_file" "python_setup_guide" {
  content = <<-EOF
# �� Interview Practice - Python Setup Guide

## Quick Start
\`\`\`bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv310

# 3. Activate virtual environment
# On Windows:
venv310\\Scripts\\activate
# On macOS/Linux:
source venv310/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Start the backend server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 6. In another terminal, start the frontend
cd ../frontend
npm install
npm run dev
\`\`\`

## Local Storage
- Files stored in: \`./uploads/\`
- Database: \`./interview_ai.db\`
- Logs: \`./logs/\`

## Features Working Locally
✅ Real-time mock interviews  
✅ Speech-to-text transcription (Vosk)  
✅ Sentiment analysis (TextBlob)  
✅ Eye-contact analysis (MediaPipe)  
✅ AI-generated feedback  
✅ File uploads and storage  

## Local Setup
- Storage: Local file system
- Database: SQLite
- AI Processing: Local models (Vosk, MediaPipe, TextBlob)
- Logs: Local files
- Monitoring: Local metrics

## Dependencies
- Python 3.10+
- ffmpeg (for audio extraction)
- Vosk model (for speech-to-text)
- MediaPipe (for eye contact analysis)
EOF
  filename = "${path.module}/PYTHON_SETUP.md"
}

#  Requirements.txt for Python Dependencies
resource "local_file" "requirements_txt" {
  content = <<-EOF
# FastAPI and web framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.23
alembic==1.12.1

# Authentication and security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Configuration
pydantic==2.5.0
pydantic-settings==2.1.0

# Local AI/ML 
opencv-python==4.8.1.78
numpy==1.24.3
scipy==1.11.4
scikit-learn==1.3.2

# Audio processing 
librosa==0.10.1
soundfile==0.12.1

# Image processing
pillow==10.1.0

# Utilities
python-dateutil==2.8.2
pytz==2023.3

# Development and testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2

# Logging
loguru==0.7.2

# CORS
fastapi-cors==0.0.6

# Rate limiting
slowapi==0.1.9

# File handling
aiofiles==23.2.1

# Redis (optional - for caching)
redis==5.0.1

# Environment variables
python-dotenv==1.0.0
EOF
  filename = "${path.module}/requirements.txt"
}

#  Vosk Model Setup Guide
resource "local_file" "vosk_setup_guide" {
  content = <<-EOF
#  Vosk Speech-to-Text Model Setup

## Download Vosk Model
1. Go to: https://alphacephei.com/vosk/models
2. Download: \`vosk-model-small-en-us-0.15.tar.gz\`
3. Extract to: \`backend/vosk-model-small-en-us-0.15/\`

## Expected Structure
\`\`\`
backend/
├── vosk-model-small-en-us-0.15/
│   └── vosk-model-small-en-us-0.15/
│       ├── am/
│       ├── conf/
│       ├── graph/
│       ├── ivector/
│       └── README
\`\`\`

## Model Path Configuration
The model path in your code should be:
\`\`\`python
vosk_model_path = "vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15"
\`\`\`

## Verification
Run this command to test:
\`\`\`python
from vosk import Model
model = Model("vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15")
print("Vosk model loaded successfully!")
\`\`\`
EOF
  filename = "${path.module}/VOSK_SETUP.md"
}

#  FFmpeg Setup Guide
resource "local_file" "ffmpeg_setup_guide" {
  content = <<-EOF
#  FFmpeg Setup Guide

## Windows Installation
1. Download from: https://ffmpeg.org/download.html
2. Extract to: \`C:\\ffmpeg\\\`
3. Add to PATH: \`C:\\ffmpeg\\bin\\\`

## macOS Installation
\`\`\`bash
brew install ffmpeg
\`\`\`

## Linux Installation
\`\`\`bash
sudo apt update
sudo apt install ffmpeg
\`\`\`

## Verification
\`\`\`bash
ffmpeg -version
\`\`\`

## Usage in Interview Practice
FFmpeg is used to extract audio from video files for speech analysis.
EOF
  filename = "${path.module}/FFMPEG_SETUP.md"
}

#  Local Monitoring Setup
resource "local_file" "monitoring_config" {
  content = <<-EOF
# Interview Practice Local Monitoring Configuration
# This simulates AWS CloudWatch monitoring

[monitoring]
enabled = true
log_level = "INFO"
metrics_path = "./metrics"

[alerts]
cpu_threshold = 80
memory_threshold = 85
disk_threshold = 90

[storage]
local_path = "./uploads"
max_file_size = "100MB"
allowed_types = ["mp4", "wav", "mp3", "jpg", "png"]

[ai_models]
vosk_model_path = "vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15"
use_local_ai = true
mock_ai_responses = false
EOF
  filename = "${path.module}/monitoring.conf"
}

#  Local Security Configuration
resource "local_file" "security_config" {
  content = <<-EOF
# Interview Practice Security Configuration
# This simulates AWS IAM and security policies



[file_upload]
max_size = "100MB"
allowed_extensions = ["mp4", "wav", "mp3", "jpg", "png"]
scan_viruses = true

[api_security]
rate_limit = 100
cors_origins = ["http://localhost:3000"]

[database]
url = "sqlite:///./interview_ai.db"
async = false
EOF
  filename = "${path.module}/security.conf"
}

#  Environment Variables Template
resource "local_file" "env_template" {
  content = <<-EOF
#  Interview Practice Configuration
# No API keys needed - everything runs locally!

# Database Configuration
DATABASE_URL=sqlite:///./interview_ai.db

# Application Configuration
APP_NAME=Interview Practice
DEBUG=True
ENVIRONMENT=development

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000

# File Upload Configuration
UPLOAD_FOLDER=./uploads
MAX_FILE_SIZE=104857600
ALLOWED_EXTENSIONS=.mp4,.wav,.mp3,.jpg,.png

# AI Configuration
USE_LOCAL_AI=True
MOCK_AI_RESPONSES=True

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# Security Configuration
RATE_LIMIT=100
ENABLE_RATE_LIMITING=True

# Monitoring Configuration
ENABLE_METRICS=True
METRICS_PATH=./metrics

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
EOF
  filename = "${path.module}/.env.template"
}

# Variables
variable "project_name" {
  description = "Project name"
  type        = string
  default     = "interview-ai"
}

variable "environment" {
  description = "Environment"
  type        = string
  default     = "local"
}

# Outputs
output "local_storage_path" {
  description = "Local storage path for files"
  value       = "./uploads"
}

output "local_database_path" {
  description = "Local database path"
  value       = "./interview_ai.db"
}

output "local_logs_path" {
  description = "Local logs path"
  value       = "./logs"
}

output "frontend_url" {
  description = "Frontend application URL"
  value       = "http://localhost:3000"
}

output "backend_url" {
  description = "Backend API URL"
  value       = "http://localhost:8000"
}

output "api_docs_url" {
  description = "API documentation URL"
  value       = "http://localhost:8000/docs"
} 