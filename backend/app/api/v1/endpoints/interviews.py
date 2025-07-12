#  API endpoints for InterviewAI platform
# handles  interview creation, analysis, file uploads, and metrics
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
import os
import uuid
from datetime import datetime
import json
import logging
import time

# imports for database, services, and models
from app.core.database import get_db
from app.services.ai_analysis import transcribe_audio, analyze_sentiment, analyze_eye_contact, extract_audio_from_video
from app.services.metrics import metrics_service
from app.core.config import settings
from app.models.interview import Interview
from app.schemas.interview import (
    Interview as InterviewSchema,
    InterviewCreate,
    InterviewUpdate,
    InterviewWithQuestions,
    InterviewAnalysis
)

#  logging for this module
logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=InterviewSchema)
async def create_interview(
    interview_data: InterviewCreate,
    db: AsyncSession = Depends(get_db)
):
    # create a new interview session in the database
    start_time = time.time()
    logger.info(f"Creating new interview: {interview_data.title}")
    
    try:
        # create new interview record with basic information
        db_interview = Interview(
            title=interview_data.title,
            interview_type=interview_data.interview_type,
            status="created"
        )
        db.add(db_interview)
        await db.commit()
        await db.refresh(db_interview)
        
        processing_time = time.time() - start_time
        logger.info(f"Interview created successfully: ID {db_interview.id} (took {processing_time:.2f}s)")
        
        # record metrics for monitoring and analytics
        metrics_service.record_interview_created(db_interview.id, interview_data.title)
        
        return db_interview
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Error creating interview: {e} (took {processing_time:.2f}s)")
        raise HTTPException(status_code=500, detail="Failed to create interview")

# async function to retrieve all interviews from the database 
# Depends(get_db) tels fastAPI to provide a db connection , fast api willcall get_db() and pass result to thsi function
@router.get("/", response_model=List[InterviewSchema])
async def get_interviews(db: AsyncSession = Depends(get_db)):
    # retrieve all interviews from the database
    start_time = time.time()
    logger.info("Fetching all interviews")
    
    try:
        result = await db.execute(select(Interview).order_by(Interview.created_at.desc()))
        interviews = result.scalars().all()
        processing_time = time.time() - start_time
        logger.info(f"Retrieved {len(interviews)} interviews (took {processing_time:.2f}s)")
        metrics_service.record_api_request("/api/v1/interviews/", "GET", 200, processing_time)
        
        return interviews
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Error fetching interviews: {e} (took {processing_time:.2f}s)")
        metrics_service.record_api_request("/api/v1/interviews/", "GET", 500, processing_time)
        raise HTTPException(status_code=500, detail="Failed to fetch interviews")

@router.get("/{interview_id}", response_model=InterviewWithQuestions)
async def get_interview(
    interview_id: int,
    db: AsyncSession = Depends(get_db)
):
    # retrieve a specific interview by its id
    start_time = time.time()
    logger.info(f"Fetching interview ID: {interview_id}")
    
    try:
        # query specific interview by id
        result = await db.execute(select(Interview).where(Interview.id == interview_id))
        interview = result.scalar_one_or_none()
        if not interview:
            logger.warning(f"Interview not found: ID {interview_id}")
            processing_time = time.time() - start_time
            metrics_service.record_api_request(f"/api/v1/interviews/{interview_id}", "GET", 404, processing_time)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found"
            )
        
        processing_time = time.time() - start_time
        logger.info(f"Interview retrieved successfully: ID {interview_id} (took {processing_time:.2f}s)")
        metrics_service.record_api_request(f"/api/v1/interviews/{interview_id}", "GET", 200, processing_time)
        return interview
    except HTTPException:
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Error fetching interview {interview_id}: {e} (took {processing_time:.2f}s)")
        metrics_service.record_api_request(f"/api/v1/interviews/{interview_id}", "GET", 500, processing_time)
        raise HTTPException(status_code=500, detail="Failed to fetch interview")
# checks the non physical attributes of person 
@router.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    # process uploaded audio file for transcription and sentiment analysis
    start_time = time.time()
    logger.info(f"Processing audio upload: {file.filename}")
    
    try:
        # save uploaded file to local storage
        file_location = f"uploads/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
        
        # process audio using local ai services 
        transcript = transcribe_audio(file_location)
        sentiment = analyze_sentiment(transcript)
        
        processing_time = time.time() - start_time
        logger.info(f"Audio processing completed: {file.filename} (took {processing_time:.2f}s)")
        metrics_service.record_api_request("/api/v1/interviews/upload-audio/", "POST", 200, processing_time)
        return {"transcript": transcript, "sentiment": sentiment}
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Audio processing failed: {file.filename} - {e} (took {processing_time:.2f}s)")
        metrics_service.record_api_request("/api/v1/interviews/upload-audio/", "POST", 500, processing_time)
        raise HTTPException(status_code=500, detail="Audio processing failed")
#this looks at physical attributes of person 
@router.post("/upload-video/")
async def upload_video(
    file: UploadFile = File(...),
    question: str = File(...),
    question_type: str = File(...),
    db: AsyncSession = Depends(get_db)
):
    # main video analysis endpoint - processes video interviews comprehensively
    start_time = time.time()
    logger.info(f"Processing video upload: {file.filename} - Question: {question[:50]}...")
    
    # import analysis functions for performance metrics calculation
    from app.services.ai_analysis import generate_interview_tips, calculate_speech_rate, count_filler_words, calculate_overall_score
    file_location = f"uploads/{file.filename}"
    
    try:
        #here you save uplaoded files to lcoal storage , then analyze eye contact using media pipe
        # computer vision and I extract audio from video using ffmpeg and  do speech analysis and then calc
         # the metrics, finally save to db 
        with open(file_location, "wb") as f:
            f.write(await file.read())
        logger.info(f"Saved uploaded file to {file_location}")

        logger.info("Starting eye contact analysis...")
        eye_contact = analyze_eye_contact(file_location)
        if not eye_contact or 'eye_contact_percentage' not in eye_contact:
            logger.error("Eye contact analysis failed.")
            processing_time = time.time() - start_time
            metrics_service.record_analysis_failure("eye_contact_analysis", processing_time)
            raise HTTPException(status_code=500, detail="Eye contact analysis failed.")
        logger.info(f"Eye contact analysis completed: {eye_contact.get('eye_contact_percentage', 0)}%")

        audio_path = file_location + ".wav"
        transcript = ""
        sentiment = {}
        duration_seconds = 0
        
        logger.info("Starting audio extraction...")
        if extract_audio_from_video(file_location, audio_path):
            # calculate audio duration for speech rate calculation
            import wave
            wf = wave.open(audio_path, "rb")
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration_seconds = frames / float(rate)
            wf.close()
            
            # transcribe audio using vosk speech recognition
            logger.info("Starting transcription...")
            transcript = transcribe_audio(audio_path)
            logger.info(f"Transcription completed: {len(transcript)} characters")
            
            # analyze sentiment using textblob nlp library
            logger.info("Starting sentiment analysis...")
            sentiment = analyze_sentiment(transcript)
            logger.info(f"Sentiment analysis completed: {sentiment.get('sentiment', 'unknown')}")
        else:
            logger.error("Audio extraction failed (ffmpeg required)")
            processing_time = time.time() - start_time
            metrics_service.record_analysis_failure("audio_extraction", processing_time)
            raise HTTPException(status_code=500, detail="Audio extraction failed (ffmpeg required)")
        
        # validate analysis results before continuing 
        if not transcript:
            logger.error("Transcription failed.")
            processing_time = time.time() - start_time
            metrics_service.record_analysis_failure("transcription", processing_time)
            raise HTTPException(status_code=500, detail="Transcription failed.")
        if not sentiment or 'polarity' not in sentiment:
            logger.error("Sentiment analysis failed.")
            processing_time = time.time() - start_time
            metrics_service.record_analysis_failure("sentiment_analysis", processing_time)
            raise HTTPException(status_code=500, detail="Sentiment analysis failed.")

        logger.info("Calculating performance metrics...")
        speech_rate = calculate_speech_rate(transcript, duration_seconds)
        filler_word_count = count_filler_words(transcript)
        overall_score = calculate_overall_score(
            eye_contact.get("eye_contact_percentage", 0),
            sentiment.get("polarity", 0),
            speech_rate,
            filler_word_count
        )
        # helper method to generate interview tips
        ai_feedback = generate_interview_tips(eye_contact, sentiment, transcript, question_type, question)
        
        logger.info(f"Performance metrics calculated - Score: {overall_score}%, Speech Rate: {speech_rate:.1f} wpm, Fillers: {filler_word_count}")

        logger.info("Saving interview to database...")
        db_interview = Interview(
            title=question[:100] if question else "Interview",
            interview_type=question_type or "general",
            status="completed",
            video_file_path=file_location,
            audio_file_path=audio_path,
            duration_seconds=int(duration_seconds),
            transcript=transcript,
            sentiment_score=sentiment.get("polarity", 0),
            confidence_score=sentiment.get("subjectivity", 0),
            eye_contact_score=eye_contact.get("eye_contact_percentage", 0),
            speech_rate=speech_rate,
            filler_word_count=filler_word_count,
            ai_feedback=json.dumps(ai_feedback),
            improvement_suggestions="", # empty for now
            overall_score=overall_score,
            completed_at=datetime.utcnow()
        )
        db.add(db_interview)
        await db.commit()
        await db.refresh(db_interview)
        
        processing_time = time.time() - start_time
        logger.info(f"Interview analysis saved with ID {db_interview.id} (total time: {processing_time:.2f}s)")
        
        # record successful analysis metrics for monitoring saves to metrics directory in backend
        metrics_service.record_analysis_success(
            db_interview.id, 
            processing_time,
            eye_contact.get("eye_contact_percentage", 0),
            sentiment.get("polarity", 0),
            speech_rate,
            overall_score
        )
        
        # return  analysis results to frontend
        return {
            "id": db_interview.id,
            "eye_contact": eye_contact,
            "transcript": transcript,
            "sentiment": sentiment,
            "speech_rate": speech_rate,
            "filler_word_count": filler_word_count,
            "overall_score": overall_score,
            "ai_feedback": ai_feedback
        }
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Error in upload-video analysis: {e} (took {processing_time:.2f}s)")
        metrics_service.record_analysis_failure("general_error", processing_time)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/{interview_id}/analysis", response_model=InterviewAnalysis)
async def get_interview_analysis(
    interview_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        # get interview and check if analysis exists
        result = await db.execute(select(Interview).where(Interview.id == interview_id))
        interview = result.scalar_one_or_none()
        if not interview:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found"
            )
        if not interview.analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not available"
            )
            
        # parse and return analysis data from json string
        analysis_data = json.loads(interview.analysis)
        return InterviewAnalysis(
            interview_id=interview_id,
            feedback=analysis_data.get('feedback', {}),
            skill_gaps=analysis_data.get('skill_gaps', {}),
            sentiment=analysis_data.get('sentiment', {}),
            eye_contact=analysis_data.get('eye_contact', {})
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching analysis for interview {interview_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch analysis")

@router.delete("/{interview_id}")
async def delete_interview(
    interview_id: int,
    db: AsyncSession = Depends(get_db)
):
    # delete an interview and its associated files
    try:
        # get interview to check if it exists
        result = await db.execute(select(Interview).where(Interview.id == interview_id))
        interview = result.scalar_one_or_none()
        if not interview:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found"
            )
            
        # delete associated files from filesystem
        if interview.audio_file and os.path.exists(interview.audio_file):
            os.remove(interview.audio_file)
        if interview.video_file and os.path.exists(interview.video_file):
            os.remove(interview.video_file)
            
        # delete interview record from database
        await db.delete(interview)
        await db.commit()
        
        logger.info(f"Interview {interview_id} deleted successfully")
        return {"success": True, "message": "Interview deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting interview {interview_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete interview")

@router.get("/metrics")
async def get_metrics():
    logger.info("Metrics endpoint accessed")
    try:
        #helper method to get metrics 
        metrics_summary = metrics_service.get_summary()
        logger.info("Metrics retrieved successfully")
        return {
            "status": "success",
            "data": metrics_summary,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error retrieving metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve metrics")

@router.get("/health/ai")
async def check_ai_health():
    # check health status of all ai services and dependencies
    logger.info("AI health check endpoint accessed")
    try:
        vosk_model_path = "vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15"
        vosk_available = os.path.exists(vosk_model_path)
        
        # check if ffmpeg is available in system path
        import subprocess
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            ffmpeg_available = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            ffmpeg_available = False
        
        # get health status for all services
        health_status = {
            "status": "healthy" if vosk_available and ffmpeg_available else "degraded",
            "services": {
                "vosk_speech_recognition": {
                    "status": "available" if vosk_available else "unavailable",
                    "path": vosk_model_path
                },
                "ffmpeg_audio_processing": {
                    "status": "available" if ffmpeg_available else "unavailable"
                },
                "mediapipe_eye_contact": "available",
                "textblob_sentiment": "available"
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"AI health check completed: {health_status['status']}")
        return health_status
    except Exception as e:
        logger.error(f"Error in AI health check: {e}")
        raise HTTPException(status_code=500, detail="AI health check failed") 