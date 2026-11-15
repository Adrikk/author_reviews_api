from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Engine = create_engine(
    "sqlite:///./redaction.db", pool_pre_ping=True, pool_recycle=3600
)

LocalSession = sessionmaker(bind=Engine)
