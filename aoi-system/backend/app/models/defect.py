"""
Defect Model - 瑕疵記錄模型
"""

from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import BaseModel


class Defect(BaseModel):
    """瑕疵記錄表"""

    __tablename__ = 'defects'

    cell_id = Column(UUID(as_uuid=True), ForeignKey('cells.id', ondelete='CASCADE'), nullable=False)
    defect_type = Column(String(50), nullable=False)  # 瑕疵類型
    position_x = Column(Integer, nullable=False)  # X座標（像素）
    position_y = Column(Integer, nullable=False)  # Y座標（像素）
    area = Column(Numeric(10, 2), nullable=False)  # 面積（像素²）
    width = Column(Numeric(10, 2), nullable=True)  # 寬度（像素）
    height = Column(Numeric(10, 2), nullable=True)  # 高度（像素）
    bbox_x1 = Column(Integer, nullable=True)  # 邊界框左上X
    bbox_y1 = Column(Integer, nullable=True)  # 邊界框左上Y
    bbox_x2 = Column(Integer, nullable=True)  # 邊界框右下X
    bbox_y2 = Column(Integer, nullable=True)  # 邊界框右下Y
    confidence = Column(Numeric(5, 2), nullable=True)  # 置信度(%)

    # Relationships
    cell = relationship('Cell', back_populates='defects')

    def __repr__(self):
        return f"<Defect(type='{self.defect_type}', area={self.area})>"
