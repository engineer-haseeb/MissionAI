from sqlmodel import SQLModel, create_engine, Session, select
from models import Goal, Task, AccountabilityLog, ResearchPaper, PhDRadar, ScholarshipTracker
from typing import Optional, List
from datetime import datetime, date

sqlite_url = "sqlite:///mission_control_v4.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

# GOAL FUNCTIONS
def add_goal(title: str, category: str, priority: str, deadline: Optional[date] = None):
    with Session(engine) as session:
        goal = Goal(title=title, category=category, priority=priority, deadline=deadline)
        session.add(goal)
        session.commit()
        session.refresh(goal)
        return goal

def get_all_goals():
    with Session(engine) as session:
        return list(session.exec(select(Goal).where(Goal.is_archived == False)).all())

def delete_goal(goal_id: int):
    with Session(engine) as session:
        goal = session.exec(select(Goal).where(Goal.id == goal_id)).first()
        if goal:
            session.delete(goal)
            session.commit()

# TASK/KANBAN FUNCTIONS
def add_task(title: str, category: str, priority: str, goal_id: Optional[int] = None, est_time: float = 1.0, due_date: Optional[date] = None):
    with Session(engine) as session:
        task = Task(title=title, category=category, priority=priority, goal_id=goal_id, estimated_time=est_time, due_date=due_date)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

def get_all_tasks():
    with Session(engine) as session:
        return list(session.exec(select(Task)).all())

def update_kanban_status(task_id: int, new_status: str, actual_time: float = 0.0):
    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.id == task_id)).first()
        if task:
            task.kanban_status = new_status
            task.is_completed = True if new_status == "Done" else False
            if actual_time > 0:
                task.actual_time = actual_time
            session.add(task)
            session.commit()

# ACCOUNTABILITY & ANALYTICS DATA CORE
def set_morning_checkin(date_str: str, sleep: float, mood: int, energy: int, hours: float):
    with Session(engine) as session:
        log = session.exec(select(AccountabilityLog).where(AccountabilityLog.log_date == date_str)).first()
        if not log:
            log = AccountabilityLog(log_date=date_str)
        log.sleep_hours = sleep
        log.morning_mood = mood
        log.morning_energy = energy
        log.available_hours = hours
        session.add(log)
        session.commit()
        return log

def log_focus_hours(date_str: str, hours: float):
    with Session(engine) as session:
        log = session.exec(select(AccountabilityLog).where(AccountabilityLog.log_date == date_str)).first()
        if not log:
            log = AccountabilityLog(log_date=date_str)
        log.focus_hours += hours
        session.add(log)
        session.commit()

def set_night_review(date_str: str, comp_count: int, reason: str, recovery: str):
    with Session(engine) as session:
        log = session.exec(select(AccountabilityLog).where(AccountabilityLog.log_date == date_str)).first()
        if log:
            log.night_completed_count = comp_count
            log.night_missed_reason = reason
            log.recovery_plan = recovery
            session.add(log)
            session.commit()
        return log

def get_accountability_log(date_str: str):
    with Session(engine) as session:
        return session.exec(select(AccountabilityLog).where(AccountabilityLog.log_date == date_str)).first()

def get_all_accountability_logs():
    with Session(engine) as session:
        return list(session.exec(select(AccountabilityLog)).all())

# RESEARCH PAPERS DATA
def add_research_paper(title: str, authors: str, year: int, methodology: str, findings: str, gaps: str, goal_id: Optional[int] = None, journal: str = None):
    with Session(engine) as session:
        paper = ResearchPaper(title=title, authors=authors, year=year, core_methodology=methodology, key_findings=findings, limitations_gaps=gaps, goal_id=goal_id, journal=journal)
        session.add(paper)
        session.commit()
        session.refresh(paper)
        return paper

def get_all_papers():
    with Session(engine) as session:
        return list(session.exec(select(ResearchPaper)).all())

# PHD STUDIO TRACKER & USA APP EXTENSIONS
def add_phd_target(univ: str, name: str, email: str, status: str, match_score: int, abstract: str):
    with Session(engine) as session:
        target = PhDRadar(university=univ, professor_name=name, professor_email=email, email_status=status, research_match_score=match_score, professor_research=abstract)
        session.add(target)
        session.commit()
        session.refresh(target)
        return target

def get_all_phd_targets():
    with Session(engine) as session:
        return list(session.exec(select(PhDRadar)).all())

def update_email_studio(target_id: int, status: str, draft: Optional[str] = None, acceptance: str = "Pending", notes: Optional[str] = None):
    with Session(engine) as session:
        target = session.exec(select(PhDRadar).where(PhDRadar.id == target_id)).first()
        if target:
            target.email_status = status
            target.acceptance_status = acceptance
            if draft:
                target.generated_draft = draft
            if notes:
                target.interview_notes = notes
            target.updated_at = datetime.utcnow()
            session.add(target)
            session.commit()

# SCHOLARSHIP TRACKER PIPELINE OPERATIONS
def add_scholarship(name: str, status: str, deadline: Optional[date], checklist: str):
    with Session(engine) as session:
        sch = ScholarshipTracker(name=name, status=status, deadline=deadline, doc_checklist=checklist)
        session.add(sch)
        session.commit()
        session.refresh(sch)
        return sch

def get_all_scholarships():
    with Session(engine) as session:
        return list(session.exec(select(ScholarshipTracker)).all())

def update_scholarship_status(sch_id: int, status: str, history: Optional[str] = None, checklist: Optional[str] = None):
    with Session(engine) as session:
        sch = session.exec(select(ScholarshipTracker).where(ScholarshipTracker.id == sch_id)).first()
        if sch:
            sch.status = status
            if history:
                sch.submission_history = history
            if checklist is not None:
                sch.doc_checklist = checklist
            session.add(sch)
            session.commit()