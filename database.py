from sqlmodel import SQLModel, create_engine, Session, select
from models import Task

sqlite_url = "sqlite:///mission_control.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

def add_task(title: str, category: str):
    with Session(engine) as session:
        new_task = Task(title=title, category=category)
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return new_task

def get_all_tasks():
    with Session(engine) as session:
        statement = select(Task)
        return list(session.exec(statement).all())

def update_task_status(task_id: int, is_completed: bool):
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id)
        task = session.exec(statement).first()
        if task:
            task.is_completed = is_completed
            session.add(task)
            session.commit()