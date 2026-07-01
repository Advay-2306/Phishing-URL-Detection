from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

Base = declarative_base()

def get_db_url():
    db_path = Path("logs/phishing_logs.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)  # ensure logs folder exists
    return f"sqlite:///{db_path.absolute()}"

engine = create_engine(get_db_url(), echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)