from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

Engine = create_engine(
    "sqlite:///./redaction.db", pool_pre_ping=True, pool_recycle=3600
)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


LocalSession = sessionmaker(bind=Engine)
