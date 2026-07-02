from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

# ==========================================
# 1. STRATEGIC GOALS SCHEMA
# ==========================================
class Goal(SQLModel, table=True):
    __tablename__ = "goals"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    category: str = Field(default="Research", index=True)  
    priority: int = Field(default=3)                       
    target_date: datetime = Field(default_factory=datetime.utcnow)
    is_archived: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    tasks: List["Task"] = Relationship(back_populates="goal")

# ==========================================
# 2. CORE PAYLOAD TASKS SCHEMA
# ==========================================
class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    goal_id: Optional[int] = Field(default=None, foreign_key="goals.id")
    title: str = Field(index=True)
    category: str = Field(index=True)
    priority: str = Field(default="Medium")                 
    estimated_time: float = Field(default=1.0)             
    is_completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    goal: Optional[Goal] = Relationship(back_populates="tasks")

# ==========================================
# 3. SCHOLARSHIP TRACKER SCHEMA
# ==========================================
class Scholarship(SQLModel, table=True):
    __tablename__ = "scholarships"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)                           
    country: str = Field(default="China")
    deadline: str = Field(default="2027-03-01")             
    status: str = Field(default="Drafting")                
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
    email_status: str = Field(default="Not Sent")          
    notes: Optional[str] = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.utcnow)