"""
Database Configuration and Session Management
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/aoi_system'
)

# Create Engine
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=True,  # Set to False in production
    pool_pre_ping=True,
    connect_args={
        'connect_timeout': 10,
    }
)

# Create Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Thread-safe session
Session = scoped_session(SessionLocal)


def get_db():
    """
    Get database session (for Flask context)
    Usage:
        db = get_db()
        try:
            # Your database operations
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables
    Usage: Call this function to create all tables
    """
    from app.models import Base
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


def drop_db():
    """
    Drop all database tables
    WARNING: This will delete all data!
    """
    from app.models import Base
    Base.metadata.drop_all(bind=engine)
    print("🗑️  All database tables dropped!")
