"""
Lot Model - 批次模型
"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel


class Lot(BaseModel):
    """批次表"""

    __tablename__ = 'lots'

    lot_number = Column(String(100), unique=True, nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False, default='CREATED')
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    inspections = relationship('Inspection', back_populates='lot', cascade='all, delete-orphan')
    merged_inspections = relationship('MergedInspection', back_populates='lot', cascade='all, delete-orphan')
    marking_card_params = relationship('MarkingCardParam', back_populates='lot', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Lot(lot_number='{self.lot_number}', status='{self.status}')>"
