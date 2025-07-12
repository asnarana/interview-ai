# Local Development Outputs

# Thisfile will define what info to show after running

output "setup_instructions" {
  description = "Quick setup instructions"
  value       = "Run: cd backend && python -m uvicorn app.main:app --reload"
}

output "python_version" {
  description = "Required Python version"
  value       = "Python 3.10+"
}

output "vosk_model_path" {
  description = "Vosk model path"
  value       = "vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15"
}

output "database_type" {
  description = "Database type and configuration"
  value       = "SQLite (local file-based)"
}

output "ai_processing" {
  description = "AI processing method"
  value       = "Local models (Vosk, MediaPipe, TextBlob)"
} 