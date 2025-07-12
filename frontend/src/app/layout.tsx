// next.js metadata type for seo optimization
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
// inter font with latin character subset for better performance
const inter = Inter({ subsets: ['latin'] })
// seo metadata configuration for the application
export const metadata: Metadata = {
  title: 'Interview Practice - AI-Powered Interview Coaching',
  description: 'Transform your interview preparation with AI-driven coaching, real-time feedback, and personalized improvement recommendations.',
  keywords: 'interview, AI, coaching, preparation, feedback, career',
  authors: [{ name: 'InterviewAI Team' }],
  viewport: 'width=device-width, initial-scale=1', 
}
// root layout component - wraps all pages in the application
export default function RootLayout({
  children, // all page content gets passed here
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      {/* apply inter font to the entire body */}
      <body className={inter.className}>
        {/* main container with gradient background and dark mode support */}
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
          {/* child components here  */}
          {children}
        </div>
      </body>
    </html>
  )
} 