from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

# ==========================================
# 1. GOALS SCHEMA
# ==========================================
class Goal(SQLModel, table=True):
    __tablename__ = "goals"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    category: str = Field(default="Research", index=True)  # Research, Cloud AI, HSK4, Gym, Career
    priority: int = Field(default=3)                       # Rating 1 to 5 Stars
    target_date: datetime = Field(default_factory=datetime.utcnow)
    is_archived: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    tasks: List["Task"] = Relationship(back_populates="goal")

# ==========================================
# 2. TASKS SCHEMA
# ==========================================
class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    goal_id: Optional[int] = Field(default=None, foreign_key="goals.id")
    title: str = Field(index=True)
    category: str = Field(index=True)
    priority: str = Field(default="Medium")                 # High, Medium, Low
    estimated_time: float = Field(default=1.0)             # Metric in Hours
    is_completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    goal: Optional[Goal] = Relationship(back_populates="tasks")
    # ==========================================
# 3. SCHOLARSHIP TRACKER SCHEMA
# ==========================================
class Scholarship(SQLModel, table=True):
    __tablename__ = "scholarships"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)                           # e.g., ANSO, CSC, President Scholarship
    country: str = Field(default="China")
    deadline: str = Field(default="2027-03-01")             # Standard Date String
    status: str = Field(default="Drafting")                # Drafting, Applied, Shortlisted, Accepted, Rejected
    notes: Optional[str] = Field(default=None)

# ==========================================
# 4. PHD APPLICATION RADAR SCHEMA
# ==========================================
class PhDRadar(SQLModel, table=True):
    __tablename__ = "phd_radar"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    university: str = Field(index=True)
    professor_name: str
    professor_email: str
    email_status: str = Field(default="Not Sent")          # Not Sent, Cold Email Sent, Replied (Positive), Replied (Negative), Interview Scheduled
    notes: Optional[str] = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.utcnow)