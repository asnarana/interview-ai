# ai analysis service using local models for speech-to-text, sentiment, and eye contact analysis
import json
import random
from typing import Dict, List, Optional
import logging
from vosk import Model, KaldiRecognizer
import wave
from textblob import TextBlob
import cv2
import mediapipe as mp
import subprocess
import os
import re

logger = logging.getLogger(__name__)

vosk_model_path = "vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15"
vosk_model = Model(vosk_model_path)

def transcribe_audio(file_path):
    #transcribe audio file using vosk speech recognition
    # open wave file for reading
    wf = wave.open(file_path, "rb")
    rec = KaldiRecognizer(vosk_model, wf.getframerate())
    rec.SetWords(True)
    results = []
    
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            results.append(json.loads(rec.Result()))
    
    results.append(json.loads(rec.FinalResult()))
    # combine all transcribed text
    transcript = " ".join([r.get("text", "") for r in results])
    return transcript

def analyze_sentiment(text):
    # create textblob object for sentiment analysis
    blob = TextBlob(text)
    # get polarity score (-1 to 1, where -1 is negative, 1 is positive)
    polarity = blob.sentiment.polarity
    
    # classify sentiment based on polarity threshold
    if polarity > 0.1:
        sentiment = "positive"
    elif polarity < -0.1:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return {"sentiment": sentiment, "polarity": polarity}

def analyze_eye_contact(video_path):
    #mediapipe face mesh for facial landmark detection
    mp_face_mesh = mp.solutions.face_mesh
    cap = cv2.VideoCapture(video_path)
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    eye_contact_frames = 0
    total_frames = 0

    # process each frame in the video
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        total_frames += 1
        # convert bgr to rgb for mediapipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            # left and right eye center landmarks (33 and 263)
            left_eye = landmarks[33]
            right_eye = landmarks[263]
            # if both eyes are horizontally centered (x between 0.4 and 0.6), count as eye contact
            if 0.4 < left_eye.x < 0.6 and 0.4 < right_eye.x < 0.6:
                eye_contact_frames += 1
    cap.release()
    face_mesh.close()
    
    # calculate percentage of frames with good eye contact
    if total_frames == 0:
        return {"eye_contact_percentage": 0}
    return {"eye_contact_percentage": 100 * eye_contact_frames / total_frames}

def extract_audio_from_video(video_path, output_wav_path):
    try:
        # use ffmpeg to extract audio as wav format
        command = [
            "ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", output_wav_path
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return os.path.exists(output_wav_path)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # if ffmpeg is not available, return false and continue without audio analysis
        print("Warning: ffmpeg not found. Audio analysis will be skipped.")
        return False

def generate_interview_tips(eye_contact, sentiment, transcript, question_type, question):
    tips = []
    # eye contact feedback
    if eye_contact.get("eye_contact_percentage", 100) < 70:
        tips.append("Try to look at the camera more often to improve your eye contact.")
    
    # transcript and question analysis
    transcript_lower = transcript.lower()
    question_lower = question.lower()
    # check if the answer is relevant to the question
    if question_type == "behavioral":
        if len(transcript.split()) < 20:
            tips.append("For behavioral questions, use the STAR method (Situation, Task, Action, Result) and give a detailed story.")
        if not any(word in transcript_lower for word in ["situation", "task", "action", "result"]):
            tips.append("Try to structure your answer using the STAR method keywords.")
        if sentiment.get("sentiment") == "negative":
            tips.append("Frame your answer positively, even if discussing a challenge. Focus on what you learned or how you improved.")
        if sentiment.get("sentiment") == "neutral":
            tips.append("Add more emotion or personal reflection to your answer.")
    elif question_type == "technical":
        if len(transcript.split()) < 20:
            tips.append("For technical questions, explain the concept step by step and give a real-world example if possible.")
        if "example" not in transcript_lower:
            tips.append("Try to include a real-world example in your technical answer.")
        if not any(word in transcript_lower for word in question_lower.split()):
            tips.append("Make sure your answer directly addresses the technical question asked.")
        tips.append("Focus on clarity and structure. If you can, mention trade-offs or alternatives.")
    elif question_type == "general":
        if len(transcript.split()) < 20:
            tips.append("For general questions, expand on your answer to show your motivation and goals.")
        if sentiment.get("sentiment") == "negative":
            tips.append("Show confidence and motivation in your answer.")
        if not any(word in transcript_lower for word in question_lower.split()):
            tips.append("Make sure your answer is relevant to the question.")
    
    if len(transcript.split()) < 5:
        tips.append("Try to give a more complete answer with specific details.")
    if not tips:
        tips.append("Great job! Your answer matches what we'd expect for this question.")
    
    return tips

def calculate_speech_rate(transcript: str, duration_seconds: float) -> float:
    if not transcript or not duration_seconds or duration_seconds == 0:
        return 0.0
    
    # count words in transcript
    word_count = len(transcript.split())
    minutes = duration_seconds / 60.0
    return word_count / minutes if minutes > 0 else 0.0

def count_filler_words(transcript: str) -> int:
    # define common filler words to look for
    fillers = [r'\bum\b', r'\buh\b', r'\blike\b', r'\byou know\b', r'\ber\b', r'\bso\b']
    count = 0
    # count occurrences of each filler word
    for filler in fillers:
        count += len(re.findall(filler, transcript.lower()))
    return count

def calculate_overall_score(eye_contact_percentage, sentiment_polarity, speech_rate, filler_word_count):
    # normalize metrics (0-1 scale)
    eye_score = min(max(eye_contact_percentage / 100, 0), 1)
    sentiment_score = (sentiment_polarity + 1) / 2  # polarity -1 to 1 -> 0 to 1
    
    # assume ideal speech rate is 90-130 wpm
    if speech_rate < 90:
        speech_score = speech_rate / 90
    elif speech_rate > 130:
        speech_score = max(0, 1 - (speech_rate - 130) / 70)
    else:
        speech_score = 1
    speech_score = min(max(speech_score, 0), 1)
    
    # fewer fillers means the better, 0 is best
    filler_score = max(0, 1 - (filler_word_count / 10))  # 0 fillers = 1, 10+ = 0
    # weighted average of all metrics
    overall = 0.3 * eye_score + 0.3 * sentiment_score + 0.2 * speech_score + 0.2 * filler_score
    return round(overall * 100, 1)  # as percentage 