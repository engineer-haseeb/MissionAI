from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime, date

# 1. STRATEGIC GOALS & MILESTONES
class Goal(SQLModel, table=True):
    __tablename__ = "goals"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    category: str = Field(default="Research", index=True) # Research, PhD, Scholarship, Learning, Health, Finance, Personal
    priority: str = Field(default="Medium")               # Critical, High, Medium, Low
    progress_pct: float = Field(default=0.0)
    deadline: Optional[date] = Field(default=None)
    is_archived: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    tasks: List["Task"] = Relationship(back_populates="goal")
    papers: List["ResearchPaper"] = Relationship(back_populates="goal")

# 2. CORE EXECUTION MATRIX (KANBAN & DEPENDENCIES)
class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    goal_id: Optional[int] = Field(default=None, foreign_key="goals.id")
    title: str = Field(index=True)
    category: str = Field(index=True)
    priority: str = Field(default="Medium")
    estimated_time: float = Field(default=1.0)           # In hours
    actual_time: float = Field(default=0.0)              # For tracking productivity analytics
    kanban_status: str = Field(default="Todo", index=True) # Todo, In Progress, Blocked, Done
    is_completed: bool = Field(default=False, index=True)
    due_date: Optional[date] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    goal: Optional[Goal] = Relationship(back_populates="tasks")

# 3. ACCOUNTABILITY & PERFORMANCE ANALYTICS LOGS
class AccountabilityLog(SQLModel, table=True):
    __tablename__ = "accountability_logs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    log_date: str = Field(index=True, unique=True)        # YYYY-MM-DD
    sleep_hours: float = Field(default=7.0)
    morning_mood: int = Field(default=3)                  # 1-5 Scale
    morning_energy: int = Field(default=3)                # 1-5 Scale
    available_hours: float = Field(default=4.0)
    focus_hours: float = Field(default=0.0)               # Tracking deep work hours
    night_completed_count: int = Field(default=0)
    night_missed_reason: Optional[str] = Field(default=None)
    recovery_plan: Optional[str] = Field(default=None)

# 4. RESEARCH REPOSITORY (V1 INSIGHTS)
class ResearchPaper(SQLModel, table=True):
    __tablename__ = "research_papers"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    goal_id: Optional[int] = Field(default=None, foreign_key="goals.id")
    title: str = Field(index=True)
    authors: str
    year: int
    journal: Optional[str] = None
    core_methodology: str
    key_findings: str
    limitations_gaps: str
    
    goal: Optional[Goal] = Relationship(back_populates="papers")

# 5. OUTREACH RADAR & USA PHD TRACKER
class PhDRadar(SQLModel, table=True):
    __tablename__ = "phd_radar"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    university: str = Field(index=True)
    professor_name: str
    professor_email: str
    email_status: str = Field(default="Not Sent")         # Not Sent, Sent, Follow-up, Replied, Interview
    research_match_score: int = Field(default=80)          # 1-100% Match
    acceptance_status: str = Field(default="Pending")     # Pending, Accepted, Rejected
    interview_notes: Optional[str] = Field(default=None)
    professor_research: Optional[str] = None
    generated_draft: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# 6. GLOBAL SCHOLARSHIP TRACKER (ANSO / CSC / FELLOWSHIPS)
class ScholarshipTracker(SQLModel, table=True):
    __tablename__ = "scholarships"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)                         # ANSO, CSC, Fulbright, etc.
    status: str = Field(default="Drafting")                # Drafting, Submitted, Shortlisted, Awarded, Rejected
    deadline: Optional[date] = Field(default=None)
    doc_checklist: str = Field(default="")                # Comma separated items like "CV, Recommendation, Proposal"
    submission_history: Optional[str] = Field(default=None)