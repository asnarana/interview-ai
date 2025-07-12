'use client'

import { useState } from 'react'
import { 
  Mic, 
  Video, 
  Brain, 
  TrendingUp
} from 'lucide-react'
import Link from 'next/link'
// this is the page that the user sees when they go to the home page. They will see
// a list of features and a button to start a practice interview
export default function Home() {
  const [isRecording, setIsRecording] = useState(false)
  const features = [
    {
      icon: <Mic className="h-6 w-6" />,
      title: "Speech Analysis",
      description: "Advanced speech recognition and filler word detection"
    },
    {
      icon: <Brain className="h-6 w-6" />,
      title: "AI Feedback",
      description: "Personalized coaching with GPT-4o powered insights"
    },
    {
      icon: <TrendingUp className="h-6 w-6" />,
      title: "Progress Tracking",
      description: "Monitor your improvement over time with detailed analytics"
    },
    {
      icon: <Video className="h-6 w-6" />,
      title: "Video Analysis",
      description: "Eye contact and body language assessment"
    }
  ]

  const stats = [
    { label: "Active Users", value: "10,000+" },
    { label: "Interviews Analyzed", value: "50,000+" },
    { label: "Success Rate", value: "85%" },
    { label: "AI Accuracy", value: "92%" }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/*  header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Interview Practice</h1>
          <p className="text-gray-600 mt-2">Practice interviews with AI feedback</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Master Your Interview Skills
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Practice with AI-powered mock interviews and get instant feedback
          </p>
          <Link 
            href="/interview"
            className="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            Start Practice Interview
          </Link>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-blue-600 text-2xl mb-4">🎤</div>
            <h3 className="text-xl font-semibold mb-2">Speech Analysis</h3>
            <p className="text-gray-600">Get feedback on your speaking pace, clarity, and confidence</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-blue-600 text-2xl mb-4">👁️</div>
            <h3 className="text-xl font-semibold mb-2">Eye Contact</h3>
            <p className="text-gray-600">Track your eye contact and body language during interviews</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-blue-600 text-2xl mb-4">💡</div>
            <h3 className="text-xl font-semibold mb-2">AI Feedback</h3>
            <p className="text-gray-600">Receive personalized suggestions for improvement</p>
          </div>
        </div>

        {/* How It Works */}
        <div className="bg-white p-8 rounded-lg shadow-md">
          <h3 className="text-2xl font-bold mb-6 text-center">How It Works</h3>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="bg-blue-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-blue-600 font-bold">1</span>
              </div>
              <h4 className="font-semibold mb-2">Record Interview</h4>
              <p className="text-gray-600">Upload your audio/video recording</p>
            </div>
            
            <div className="text-center">
              <div className="bg-blue-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-blue-600 font-bold">2</span>
              </div>
              <h4 className="font-semibold mb-2">AI Analysis</h4>
              <p className="text-gray-600">Our AI analyzes your performance</p>
            </div>
            
            <div className="text-center">
              <div className="bg-blue-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-blue-600 font-bold">3</span>
              </div>
              <h4 className="font-semibold mb-2">Get Feedback</h4>
              <p className="text-gray-600">Receive detailed feedback and tips</p>
            </div>
          </div>
        </div>
      </main>

      {/* Simple Footer */}
      <footer className="bg-gray-800 text-white py-8 mt-12">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <p className="text-gray-300">
                Built with Next.js, FastAPI, and AI
          </p>
          <p className="text-gray-400 text-sm mt-2">
            Student project for interview practice
          </p>
        </div>
      </footer>
    </div>
  )
} 