from models import Goal, Task, Scholarship, PhDRadar  # <--- Inhein add karein top par
from typing import Optional  # <--- YEH LINE TOP PAR LAZMI CHAHIYE
from sqlmodel import SQLModel, create_engine, Session, select
sqlite_url = "sqlite:///mission_control.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

# ==========================================
# GOAL CRUD OPERATIONS
# ==========================================
def add_goal(title: str, category: str, priority: int):
    with Session(engine) as session:
        new_goal = Goal(title=title, category=category, priority=priority)
        session.add(new_goal)
        session.commit()
        session.refresh(new_goal)
        return new_goal

def get_all_goals():
    with Session(engine) as session:
        return list(session.exec(select(Goal).where(Goal.is_archived == False)).all())

# ==========================================
# TASK CRUD OPERATIONS
# ==========================================
def add_task(title: str, category: str, priority: str, goal_id: Optional[int] = None, est_time: float = 1.0):
    with Session(engine) as session:
        new_task = Task(
            title=title, 
            category=category, 
            priority=priority, 
            goal_id=goal_id, 
            estimated_time=est_time
        )
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return new_task

def get_all_tasks():
    with Session(engine) as session:
        return list(session.exec(select(Task)).all())

def update_task_status(task_id: int, is_completed: bool):
    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.id == task_id)).first()
        if task:
            task.is_completed = is_completed
            session.add(task)
            session.commit()

# Yeh line ensure karein ke database.py ke bottom me maujood ho
def delete_goal(goal_id: int):
    with Session(engine) as session:
        goal = session.exec(select(Goal).where(Goal.id == goal_id)).first()
        if goal:
            goal.is_archived = True
            session.add(goal)
            session.commit()
# ==========================================
# SCHOLARSHIP CRUD OPERATIONS
# ==========================================
def add_scholarship(name: str, country: str, deadline: str, status: str, notes: str = None):
    with Session(engine) as session:
        new_sch = Scholarship(name=name, country=country, deadline=deadline, status=status, notes=notes)
        session.add(new_sch)
        session.commit()
        session.refresh(new_sch)
        return new_sch

def get_all_scholarships():
    with Session(engine) as session:
        return list(session.exec(select(Scholarship)).all())

# ==========================================
# PHD RADAR CRUD OPERATIONS
# ==========================================
def add_phd_target(university: str, prof_name: str, prof_email: str, email_status: str, notes: str = None):
    with Session(engine) as session:
        new_target = PhDRadar(university=university, professor_name=prof_name, professor_email=prof_email, email_status=email_status, notes=notes)
        session.add(new_target)
        session.commit()
        session.refresh(new_target)
        return new_target

def get_all_phd_targets():
    with Session(engine) as session:
        return list(session.exec(select(PhDRadar)).all())

def update_email_status(target_id: int, new_status: str):
    with Session(engine) as session:
        target = session.exec(select(PhDRadar).where(PhDRadar.id == target_id)).first()
        if target:
            target.email_status = new_status
            target.updated_at = datetime.utcnow()
            session.add(target)
            session.commit()
       