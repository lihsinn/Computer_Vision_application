"""
MarkingCardParam Model - 瑕疵標註卡參數模型
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel


class MarkingCardParam(BaseModel):
    """瑕疵標註卡參數表"""

    __tablename__ = 'marking_card_params'

    lot_id = Column(UUID(as_uuid=True), ForeignKey('lots.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)  # 參數名稱
    grid_rows = Column(Integer, nullable=False)  # 網格行數
    grid_cols = Column(Integer, nullable=False)  # 網格列數
    cell_width = Column(Integer, nullable=False)  # Cell寬度（像素）
    cell_height = Column(Integer, nullable=False)  # Cell高度（像素）
    offset_x = Column(Integer, default=0)  # X偏移量
    offset_y = Column(Integer, default=0)  # Y偏移量
    output_format = Column(String(20), nullable=False)  # 'IMAGE', 'WORD', or 'PDF'
    is_active = Column(Boolean, default=True)  # 是否啟用
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    lot = relationship('Lot', back_populates='marking_card_params')

    def __repr__(self):
        return f"<MarkingCardParam(name='{self.name}', grid={self.grid_rows}x{self.grid_cols})>"
