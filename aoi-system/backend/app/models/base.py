"""
Base Model with common utilities
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

Base = declarative_base()


class BaseModel(Base):
    """Base class with common columns"""

    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        """Convert model instance to dictionary"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            elif isinstance(value, uuid.UUID):
                value = str(value)
            result[column.name] = value
        return result
