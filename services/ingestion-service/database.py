# database.py

from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime, Float
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.sql import func
import uuid

# ✅ SQLite DB (auto-created, no install needed)
DATABASE_URL = "sqlite:///./aiops.db"

# ✅ Engine (SQLite requires this flag)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# ✅ Session factory
SessionLocal = sessionmaker(bind=engine)


# ✅ Base class
class Base(DeclarativeBase):
    pass


# ✅ Incident Table
class Incident(Base):
    __tablename__ = "incidents"

    # ✅ User-friendly ID (1,2,3...)
    display_id = Column(Integer, primary_key=True, autoincrement=True)

    # ✅ Internal UUID (for system use)
    id = Column(String, unique=True, default=lambda: str(uuid.uuid4()))

    service_name = Column(String, nullable=False)
    error_message = Column(Text)
    error_count = Column(Integer, default=0)

    severity = Column(String)
    status = Column(String, default="OPEN")

    ai_analysis = Column(Text)
    sre_decision = Column(String)
    fix_applied = Column(Text)

    correlation_id = Column(String)
    trace_id = Column(String)

    total_duration_ms = Column(Float)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


# ✅ FastAPI DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()