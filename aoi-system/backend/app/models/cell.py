"""
Cell Model - Cell資料模型
"""

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import BaseModel


class Cell(BaseModel):
    """Cell資料表"""

    __tablename__ = 'cells'

    inspection_id = Column(UUID(as_uuid=True), ForeignKey('inspections.id', ondelete='CASCADE'), nullable=False)
    cell_number = Column(Integer, nullable=False)  # Cell編號（1, 2, 3...）
    position_x = Column(Integer, nullable=False)  # X座標（像素）
    position_y = Column(Integer, nullable=False)  # Y座標（像素）
    width = Column(Integer, nullable=False)  # 寬度（像素）
    height = Column(Integer, nullable=False)  # 高度（像素）
    status = Column(String(10), nullable=False)  # 'PASS' or 'NG'
    defect_count = Column(Integer, default=0)  # 瑕疵數量

    # Relationships
    inspection = relationship('Inspection', back_populates='cells')
    defects = relationship('Defect', back_populates='cell', cascade='all, delete-orphan')
    manual_reviews = relationship('ManualReview', back_populates='cell', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Cell(number={self.cell_number}, status='{self.status}', defects={self.defect_count})>"
