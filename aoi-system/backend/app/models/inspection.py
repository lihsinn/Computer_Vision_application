"""
Inspection Model - 檢測記錄模型
"""

from sqlalchemy import Column, String, Integer, Boolean, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel


class Inspection(BaseModel):
    """檢測記錄表"""

    __tablename__ = 'inspections'

    lot_id = Column(UUID(as_uuid=True), ForeignKey('lots.id', ondelete='CASCADE'), nullable=False)
    serial_number = Column(String(100), nullable=False)
    side = Column(String(1), nullable=False)  # 'A' or 'B'
    inspection_mode = Column(String(20), nullable=False)  # 'Run' or 'OfflineTest'
    inspection_type = Column(String(20), nullable=False)  # 'SingleInsp' or 'BatchInsp'
    image_path = Column(String(500), nullable=False)
    annotated_image_path = Column(String(500), nullable=True)
    running_result = Column(String(50), nullable=False)  # 'SUCCESS' or 'FAILED'
    judgment_result = Column(String(10), nullable=False)  # 'PASS' or 'NG'
    yield_rate = Column(Numeric(5, 2), nullable=False)  # 良率(%)
    ng_count = Column(Integer, nullable=False)  # NG顆數
    total_cells = Column(Integer, nullable=False)  # 總Cell數
    positioning_abnormal = Column(Boolean, default=False)  # 定位異常
    threshold = Column(Integer, nullable=True)  # 檢測閾值參數
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    lot = relationship('Lot', back_populates='inspections')
    cells = relationship('Cell', back_populates='inspection', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Inspection(serial='{self.serial_number}', side='{self.side}', result='{self.judgment_result}')>"
