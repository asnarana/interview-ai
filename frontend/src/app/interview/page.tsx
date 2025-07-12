'use client'

import React, { useRef, useState } from 'react'
import Link from 'next/link'

// interview questions organized by category for different interview types
const interviewQuestions = {
  behavioral: [
    "Tell me about a time when you had to work with a difficult team member. How did you handle it?",
    "Describe a situation where you had to learn something new quickly. What was the outcome?",
    "Give me an example of a time when you failed at something. What did you learn from it?",
    "Tell me about a project where you had to take initiative. What was the result?",
    "Describe a time when you had to persuade someone to see things your way."
  ],
  technical: [
    "Explain a technical concept to someone who has no technical background.",
    "What's the most challenging technical problem you've solved?",
    "How do you stay updated with the latest technology trends?",
    "Describe your debugging process when you encounter a bug.",
    "What's your approach to learning a new programming language or framework?"
  ],
  general: [
    "Why are you interested in this position?",
    "Where do you see yourself in 5 years?",
    "What are your greatest strengths and weaknesses?",
    "Why should we hire you over other candidates?",
    "What motivates you in your work?"
  ]
}

export default function InterviewPage() {
  // state management for recording functionality
  const [recording, setRecording] = useState(false)
  const [videoURL, setVideoURL] = useState<string | null>(null)
  const [analysis, setAnalysis] = useState<any>(null)
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [selectedCategory, setSelectedCategory] = useState<'behavioral' | 'technical' | 'general'>('behavioral')
  const [interviewStarted, setInterviewStarted] = useState(false)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const recordedChunks = useRef<Blob[]>([])
  const videoRef = useRef<HTMLVideoElement | null>(null)
  const [uploading, setUploading] = useState(false)

  // get current question set and individual question
  const currentQuestions = interviewQuestions[selectedCategory]
  const currentQuestion = currentQuestions[currentQuestionIndex]

  // initialize interview session and reset state
  const startInterview = () => {
    setInterviewStarted(true)
    setCurrentQuestionIndex(0)
    setAnalysis(null)
    setVideoURL(null)
  }

  // navigate to next question in sequence
  const nextQuestion = () => {
    if (currentQuestionIndex < currentQuestions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    }
  }

  // navigate to previous question in sequence
  const previousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
    }
  }

  // start video recording using browser media api
  const startRecording = async () => {
    setAnalysis(null)
    setVideoURL(null)
    recordedChunks.current = []
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    if (videoRef.current) {
      videoRef.current.srcObject = stream
    }
    const mediaRecorder = new MediaRecorder(stream)
    mediaRecorderRef.current = mediaRecorder
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        recordedChunks.current.push(event.data)
      }
    }
    mediaRecorder.onstop = () => {
      const blob = new Blob(recordedChunks.current, { type: 'video/webm' })
      setVideoURL(URL.createObjectURL(blob))
      // stop all media tracks to release camera/microphone
      stream.getTracks().forEach(track => track.stop())
    }
    mediaRecorder.start()
    setRecording(true)
  }

  // stop video recording
  const stopRecording = () => {
    mediaRecorderRef.current?.stop()
    setRecording(false)
  }

  // upload recorded video to backend for ai analysis
  const uploadVideo = async () => {
    if (!videoURL) return
    setUploading(true)
    const response = await fetch(videoURL)
    const blob = await response.blob()
    const file = new File([blob], 'interview.webm', { type: 'video/webm' })
    const formData = new FormData()
    formData.append('file', file)
    formData.append('question', currentQuestion)
    formData.append('question_type', selectedCategory)
    const res = await fetch('http://localhost:8000/api/v1/interviews/upload-video/', {
      method: 'POST',
      body: formData,
    })
    const data = await res.json()
    console.log('Backend analysis response:', data)
    setAnalysis(data)
    setUploading(false)
  }

  // interview setup screen - select question category
  if (!interviewStarted) {
    return (
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm">
          <div className="max-w-4xl mx-auto px-4 py-4">
            <div className="flex justify-between items-center">
              <Link href="/" className="text-xl font-bold text-gray-900">
                Interview Practice
              </Link>
              <Link href="/" className="text-blue-600 hover:text-blue-800">
                ← Back to Home
              </Link>
            </div>
          </div>
        </header>

        <main className="max-w-4xl mx-auto px-4 py-8">
          <div className="bg-white rounded-lg shadow-md p-8">
            <h1 className="text-3xl font-bold text-center mb-8">Mock Interview Setup</h1>
            
            <div className="mb-8">
              <h2 className="text-xl font-semibold mb-4">Select Question Category:</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* behavioral questions selection button */}
                <button
                  onClick={() => setSelectedCategory('behavioral')}
                  className={`p-4 rounded-lg border-2 transition-colors ${
                    selectedCategory === 'behavioral'
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <h3 className="font-semibold mb-2">Behavioral Questions</h3>
                  <p className="text-sm text-gray-600">Past experiences and situations</p>
                </button>
                {/* technical questions selection button */}
                <button
                  onClick={() => setSelectedCategory('technical')}
                  className={`p-4 rounded-lg border-2 transition-colors ${
                    selectedCategory === 'technical'
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <h3 className="font-semibold mb-2">Technical Questions</h3>
                  <p className="text-sm text-gray-600">Technical skills and knowledge</p>
                </button>
                {/* general questions selection button */}
                <button
                  onClick={() => setSelectedCategory('general')}
                  className={`p-4 rounded-lg border-2 transition-colors ${
                    selectedCategory === 'general'
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <h3 className="font-semibold mb-2">General Questions</h3>
                  <p className="text-sm text-gray-600">Career goals and motivation</p>
                </button>
              </div>
            </div>

            <div className="text-center">
              <button
                onClick={startInterview}
                className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-lg font-semibold"
              >
                Start Interview
              </button>
            </div>
          </div>
        </main>
      </div>
    )
  }

  // main interview interface
  return (
    <div className="min-h-screen bg-gray-50">
      {/* header with navigation and question counter */}
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <Link href="/" className="text-xl font-bold text-gray-900">
              Interview Practice
            </Link>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">
                Question {currentQuestionIndex + 1} of {currentQuestions.length}
              </span>
              <Link href="/" className="text-blue-600 hover:text-blue-800">
                ← Back to Home
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* main interview content area */}
      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-md p-8">
          {/* display current interview question */}
          <div className="mb-8">
            <div className="bg-blue-50 border-l-4 border-blue-500 p-6 rounded-r-lg">
              <h2 className="text-xl font-semibold text-blue-900 mb-2">Interview Question:</h2>
              <p className="text-lg text-blue-800 leading-relaxed">{currentQuestion}</p>
            </div>
          </div>

          {/* question navigation controls */}
          <div className="flex justify-between items-center mb-6">
            <button
              onClick={previousQuestion}
              disabled={currentQuestionIndex === 0}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              ← Previous
            </button>
            <span className="text-sm text-gray-600">
              {selectedCategory.charAt(0).toUpperCase() + selectedCategory.slice(1)} Questions
            </span>
            <button
              onClick={nextQuestion}
              disabled={currentQuestionIndex === currentQuestions.length - 1}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next →
            </button>
          </div>
          
          {/* video recording interface */}
          <div className="flex flex-col items-center mb-6">
            {/* live video preview */}
            <video ref={videoRef} autoPlay muted width={400} height={300} className="rounded mb-4" />
            {/* recorded video playback */}
            {videoURL && (
              <video src={videoURL} controls width={400} height={300} className="rounded mb-4" />
            )}
            {/* recording control buttons */}
            <div className="flex gap-4">
              {!recording && (
                <button
                  onClick={startRecording}
                  className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Start Recording
                </button>
              )}
              {recording && (
                <button
                  onClick={stopRecording}
                  className="px-6 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                >
                  Stop Recording
                </button>
              )}
              {videoURL && !recording && (
                <button
                  onClick={uploadVideo}
                  className="px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                  disabled={uploading}
                >
                  {uploading ? 'Uploading...' : 'Upload & Analyze'}
                </button>
              )}
            </div>
          </div>

          {/* display ai analysis results */}
          {analysis && (
            <div className="mt-8">
              <h2 className="text-lg font-semibold mb-2">Analysis Results:</h2>
              <div className="bg-gray-100 p-4 rounded">
                {/* eye contact analysis */}
                <div className="mb-2">
                  <strong>Eye Contact:</strong> {analysis.eye_contact?.eye_contact_percentage?.toFixed(1) ?? 'N/A'}%
                </div>
                {/* speech transcript */}
                <div className="mb-2">
                  <strong>Transcript:</strong> {analysis.transcript || 'N/A'}
                </div>
                {/* sentiment analysis */}
                <div className="mb-2">
                  <strong>Sentiment:</strong> {analysis.sentiment?.sentiment || 'N/A'} (Polarity: {analysis.sentiment?.polarity ?? 'N/A'})
                </div>
                {/* speech rate metrics */}
                <div className="mb-2">
                  <strong>Speech Rate:</strong> {analysis.speech_rate ? analysis.speech_rate.toFixed(1) : 'N/A'} words/min
                </div>
                {/* filler word count */}
                <div className="mb-2">
                  <strong>Filler Word Count:</strong> {analysis.filler_word_count ?? 'N/A'}
                </div>
                {/* overall performance score */}
                <div className="mb-2">
                  <strong>Overall Score:</strong> {analysis.overall_score ?? 'N/A'}%
                </div>
              </div>
              {/* personalized ai feedback tips */}
              {analysis.ai_feedback && (
                <div className="mt-4 bg-yellow-50 p-4 rounded border-l-4 border-yellow-400">
                  <h3 className="text-md font-semibold mb-2 text-yellow-800">Personalized Tips:</h3>
                  <ul className="text-yellow-700 space-y-1">
                    {analysis.ai_feedback.map((tip: string, idx: number) => (
                      <li key={idx}>• {tip}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  )
} 