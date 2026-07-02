from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, create_engine, Session, select
from models import Goal, Task, Scholarship, PhDRadar, User

sqlite_url = "sqlite:///mission_control.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

# ==========================================
# AUTH OPERATIONS
# ==========================================
def create_user(username: str, password_raw: str):
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == username)).first()
        if existing:
            return False
        new_user = User(username=username, password_hash=password_raw)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

def authenticate_user(username: str, password_raw: str):
    with Session(engine) as session:
        return session.exec(select(User).where(User.username == username, User.password_hash == password_raw)).first()

# ==========================================
# GOAL OPERATIONS
# ==========================================
def add_goal(title: str, category: str, priority: int, user_id: int):
    with Session(engine) as session:
        new_goal = Goal(title=title, category=category, priority=priority, user_id=user_id)
        session.add(new_goal)
        session.commit()
        session.refresh(new_goal)
        return new_goal

def get_user_goals(user_id: int):
    with Session(engine) as session:
        return list(session.exec(select(Goal).where(Goal.user_id == user_id, Goal.is_archived == False)).all())

def delete_goal(goal_id: int):
    with Session(engine) as session:
        goal = session.exec(select(Goal).where(Goal.id == goal_id)).first()
        if goal:
            goal.is_archived = True
            session.add(goal)
            session.commit()

# ==========================================
# TASK OPERATIONS
# ==========================================
def add_task(title: str, category: str, priority: str, user_id: int, goal_id: Optional[int] = None, est_time: float = 1.0):
    with Session(engine) as session:
        new_task = Task(title=title, category=category, priority=priority, user_id=user_id, goal_id=goal_id, estimated_time=est_time)
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return new_task

def get_user_tasks(user_id: int):
    with Session(engine) as session:
        return list(session.exec(select(Task).where(Task.user_id == user_id)).all())

def update_task_status(task_id: int, is_completed: bool):
    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.id == task_id)).first()
        if task:
            task.is_completed = is_completed
            session.add(task)
            session.commit()

# ==========================================
# SCHOLARSHIP OPERATIONS
# ==========================================
def add_scholarship(name: str, country: str, deadline: str, status: str, user_id: int, notes: str = None):
    with Session(engine) as session:
        new_sch = Scholarship(name=name, country=country, deadline=deadline, status=status, user_id=user_id, notes=notes)
        session.add(new_sch)
        session.commit()
        session.refresh(new_sch)
        return new_sch

def get_user_scholarships(user_id: int):
    with Session(engine) as session:
        return list(session.exec(select(Scholarship).where(Scholarship.user_id == user_id)).all())

# ==========================================
# PHD RADAR OPERATIONS
# ==========================================
def add_phd_target(university: str, prof_name: str, prof_email: str, email_status: str, user_id: int, notes: str = None):
    with Session(engine) as session:
        new_target = PhDRadar(university=university, professor_name=prof_name, professor_email=prof_email, email_status=email_status, user_id=user_id, notes=notes)
        session.add(new_target)
        session.commit()
        session.refresh(new_target)
        return new_target

def get_user_phd_targets(user_id: int):
    with Session(engine) as session:
        return list(session.exec(select(PhDRadar).where(PhDRadar.user_id == user_id)).all())

def update_email_status(target_id: int, new_status: str):
    with Session(engine) as session:
        target = session.exec(select(PhDRadar).where(PhDRadar.id == target_id)).first()
        if target:
            target.email_status = new_status
            target.updated_at = datetime.utcnow()
            session.add(target)
            session.commit()