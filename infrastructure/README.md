# Infrastructure - Terraform Configuration

Infrastructure as Code (IaC) setup for this interview assistant using Terraform.

## Structure

```
infrastructure/
├── terraform/
│   ├── main.tf          # Local configuration
│   ├── variables.tf     # Variable definitions
│   ├── outputs.tf       # Output values
│   └── README.md        # This file
└── README.md            # Overview
```

## Local Resources
- **File Storage** - `./uploads/` for recordings
- **Database** - SQLite database
- **Logging** - `./logs/` for application logs
- **Configuration** - Environment setup files
- **Monitoring** - Metrics configuration

## Quick Setup

```bash
# 1. Initialize and apply Terraform
cd infrastructure/terraform
terraform init
terraform apply

# 2. Start application
cd ../..
docker-compose up -d

# 3. Access
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## What Terraform Creates

### Files
- `config.json` - Application configuration
- `docker-compose.override.yml` - Docker setup
- `monitoring.conf` - Monitoring config
- `security.conf` - Security settings
- `LOCAL_DEVELOPMENT.md` - Setup guide

### Directories
- `./uploads/` - File storage
- `./logs/` - Application logs
- `./metrics/` - Performance metrics

## Features Working Locally
✅ Real-time mock interviews  
✅ Speech-to-text transcription  
✅ Sentiment analysis  
✅ Eye-contact analysis  
✅ AI-generated feedback  
✅ File uploads and storage  
✅ Interview history  

## Security
- **Local Storage** - Files on your computer
- **No Internet** - Completely offline
- **SQLite** - Local database with permissions
- **JWT Tokens** - Local session management
- **CORS** - Configured for localhost
