##  AI-Powered Mock Interview Platform

**Complete mock interview platform with AI analysis**

You can just practice your interview skills by recording and then uploading the file. I used numerous ML models such as Vosk and TextBlob along with FastAPI to essentially transcribe the audio as text and used that text to analyze sentiment, speech patterns, and generate personalized feedback. This feedback included eye contact analysis using MediaPipe, speech rate calculations, filler word detection, and overall performance scoring. I also used Terraform to automate the setup process. Terraform automatically generates all the setup files, environment templates, and documentation so anyone can clone the repo and get started in minutes instead of hours. I used this to learn more about the code mechanisms to create documentations using the terraform cli and commands such as init and apply. 

## Features
- 🎤 **Speech-to-Text** - Local transcription using Vosk
- 😊 **Sentiment Analysis** - Local keyword-based analysis  
- 👁️ **Eye Contact Analysis** - Computer vision using MediaPipe
- 💬 **AI Feedback** - Template-based feedback system
- 📊 **Performance Scoring** - Multi-metric evaluation
- 📹 **Real-time Interviews** - Video/audio upload and analysis

## Tech Stack
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.10+, SQLAlchemy
- **Database**: SQLite
- **AI/ML**: Local processing (Vosk, MediaPipe, TextBlob)
- **Infrastructure**: Terraform

## AI/ML Components

### TextBlob - Sentiment Analysis
TextBlob is used for **sentiment analysis** of interview responses. It analyzes the emotional tone of transcribed speech by:
- **Polarity Scoring**: Measures sentiment from -1 (negative) to +1 (positive)
- **Sentiment Classification**: Categorizes responses as positive, negative, or neutral
- **Interview Feedback**: Provides insights on confidence, enthusiasm, and emotional delivery

### Vosk - Speech-to-Text
- **Local Transcription**: Converts audio/video to text without cloud services
- **Real-time Processing**: Handles interview recordings efficiently
- **Word-level Timing**: Provides precise timing for speech rate analysis

### MediaPipe - Eye Contact Analysis
- **Facial Landmark Detection**: Tracks eye positions in video frames
- **Eye Contact Percentage**: Calculates how often you look at the camera
- **Performance Metrics**: Integrates with overall interview scoring

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- FFmpeg (for audio processing)

### Local Development

```bash
# 1. Clone and setup backend
git clone <your-repo-url>
cd interview-ai/backend

# Create virtual environment
python -m venv venv310
venv310\Scripts\activate  # Windows
source venv310/bin/activate  # Linux/Mac

# Install and start backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
```bash
# 2. Setup frontend (new terminal)
cd frontend
npm install
npm run dev
```
### Docker Setup (Alternative)
```bash
docker-compose up -d
```
### Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Infrastructure (Terraform)

```bash
cd infrastructure/terraform
terraform init
terraform apply
```

**Generates**: Setup guides, config templates, dependency lists, documentation

## Project Structure
```
interview-ai/
├── frontend/          # Next.js React app
├── backend/           # FastAPI Python app
│   ├── app/          # API, models, services
│   ├── uploads/      # File storage
│   └── logs/         # Application logs
└── infrastructure/   # Terraform config

```
## Development
```bash
# Backend
cd backend && python -m uvicorn app.main:app --reload
# Frontend  
cd frontend && npm run dev
# Full stack
docker-compose up -d
```
## Monitoring

- **Logs**: `backend/logs/app.log`
- **Metrics**: `backend/metrics/`
- **Health**: `/health` endpoint
- **AI Status**: `/api/v1/interviews/health/ai`
