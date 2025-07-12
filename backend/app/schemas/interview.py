#  schemas for interview data validation and serialization
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# client sends json data for new interview, schema validates it( ensures req fields), model stores saves to db with al lfields 
# the schema only returns exposed fields to client 
# base interview model with common fields
class InterviewBase(BaseModel):
    title: str  # interview title/name
    interview_type: Optional[str] = None  # type of interview (e.g., technical, behavioral)
    status: Optional[str] = None  # current status (e.g., draft, completed)

class InterviewCreate(InterviewBase):
    pass  
class InterviewUpdate(InterviewBase):
    pass  

class Interview(InterviewBase):
    id: int  # unique database identifier
    created_at: Optional[str] = None  # timestamp when interview was created
    updated_at: Optional[str] = None  # timestamp when interview was last updated
    
    class Config:
        from_attributes = True  # enables orm compatibility for sqlalchemy models

# extended interview model for responses with questions
class InterviewWithQuestions(Interview):
    # simplified - no longer needs questions since they're handled in frontend
    pass  

# schema for interview analysis results
class InterviewAnalysis(BaseModel):
    interview_id: int  
    feedback: Optional[dict] = None  
    skill_gaps: Optional[dict] = None  
    sentiment: Optional[dict] = None 
    eye_contact: Optional[dict] = None  