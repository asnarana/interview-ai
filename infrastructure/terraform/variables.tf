#  Interview Practice - Local Development Variables
# this file defines what inputs terraform configuration accepts 
variable "app_name" {
  description = "Name of the application"
  type        = string
  default     = "Interview Practice"
}


variable "debug" {
  description = "Enable debug mode"
  type        = bool
  default     = true
}

variable "port" {
  description = "Port for the backend server"
  type        = number
  default     = 8000
}

variable "frontend_port" {
  description = "Port for the frontend server"
  type        = number
  default     = 3000
}

variable "local_storage_path" {
  description = "Local path for file storage"
  type        = string
  default     = "./uploads"
}

variable "local_database_path" {
  description = "Local path for SQLite database"
  type        = string
  default     = "./interview_ai.db"
}

variable "local_logs_path" {
  description = "Local path for application logs"
  type        = string
  default     = "./logs"
} 