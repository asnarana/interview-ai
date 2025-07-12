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
