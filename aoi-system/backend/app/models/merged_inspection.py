"""
MergedInspection Model - AB面合併記錄模型
"""

from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import BaseModel


class MergedInspection(BaseModel):
    """AB面合併記錄表"""

    __tablename__ = 'merged_inspections'

    lot_id = Column(UUID(as_uuid=True), ForeignKey('lots.id', ondelete='CASCADE'), nullable=False)
    serial_number = Column(String(100), nullable=False)  # 序號
    side_a_inspection_id = Column(UUID(as_uuid=True), ForeignKey('inspections.id', ondelete='CASCADE'), nullable=False)
    side_b_inspection_id = Column(UUID(as_uuid=True), ForeignKey('inspections.id', ondelete='CASCADE'), nullable=False)
    merged_judgment = Column(String(10), nullable=False)  # 'PASS' or 'NG'
    merged_yield_rate = Column(Numeric(5, 2), nullable=False)  # 合併良率(%)
    merged_ng_count = Column(Integer, nullable=False)  # 合併NG顆數

    # Relationships
    lot = relationship('Lot', back_populates='merged_inspections')
    side_a_inspection = relationship('Inspection', foreign_keys=[side_a_inspection_id])
    side_b_inspection = relationship('Inspection', foreign_keys=[side_b_inspection_id])

    def __repr__(self):
        return f"<MergedInspection(serial='{self.serial_number}', judgment='{self.merged_judgment}')>"
