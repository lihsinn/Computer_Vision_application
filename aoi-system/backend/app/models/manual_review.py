"""
ManualReview Model - 人工覆判模型
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel


class ManualReview(BaseModel):
    """人工覆判表"""

    __tablename__ = 'manual_reviews'

    cell_id = Column(UUID(as_uuid=True), ForeignKey('cells.id', ondelete='CASCADE'), nullable=False)
    original_status = Column(String(10), nullable=False)  # 原始狀態
    reviewed_status = Column(String(10), nullable=False)  # 覆判後狀態
    reviewer = Column(String(100), nullable=True)  # 覆判人員
    review_mode = Column(String(20), nullable=False)  # 'MULTI' or 'SINGLE'
    notes = Column(Text, nullable=True)  # 備註
    reviewed_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    cell = relationship('Cell', back_populates='manual_reviews')

    def __repr__(self):
        return f"<ManualReview(original='{self.original_status}', reviewed='{self.reviewed_status}')>"
