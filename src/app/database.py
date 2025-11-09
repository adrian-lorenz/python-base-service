from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.app.config.settings import DATABASE_URL

# Erstelle SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Automatische Überprüfung der Verbindung vor Verwendung
)

# Erstelle Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base-Klasse für alle Modelle
Base = declarative_base()


# Dependency Injection für DB Sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
