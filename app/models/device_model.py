from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base


class Device(Base):
    __tablename__ = "devices"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    serial      = Column(String, unique=True, nullable=False, index=True)
    brand       = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    is_available = Column(Boolean, default=True)
    created_at  = Column(DateTime, default=datetime.utcnow)

    loans = relationship("Loan", back_populates="device")
