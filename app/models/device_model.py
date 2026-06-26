<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
=======
from sqlalchemy import Column, Integer, String, Boolean, DateTime
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base


class Device(Base):
<<<<<<< HEAD
    __tablename__ = "devices"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    serial      = Column(String, unique=True, nullable=False, index=True)
    brand       = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    is_available = Column(Boolean, default=True)
    created_at  = Column(DateTime, default=datetime.utcnow)

=======
    """Modelo SQLAlchemy que representa la tabla 'devices' en la base de datos."""

    __tablename__ = "devices"

    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String, nullable=False)
    serial_number = Column(String, unique=True, nullable=False, index=True)
    device_type   = Column(String, nullable=False)
    brand         = Column(String, nullable=True)
    is_available  = Column(Boolean, default=True)
    created_at    = Column(DateTime, default=datetime.utcnow)

    # Un dispositivo puede aparecer en muchos préstamos históricos
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf
    loans = relationship("Loan", back_populates="device")
