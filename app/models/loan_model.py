<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
=======
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base


class Loan(Base):
<<<<<<< HEAD
=======
    """Modelo SQLAlchemy que representa la tabla 'loans' (préstamos)."""

>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf
    __tablename__ = "loans"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_id   = Column(Integer, ForeignKey("devices.id"), nullable=False)
    loan_date   = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
<<<<<<< HEAD
    is_returned = Column(Boolean, default=False)
    notes       = Column(String, nullable=True)

    user   = relationship("User")
=======
    status      = Column(String, nullable=False, default="active")  # active | returned | overdue

    # Cada préstamo pertenece a un usuario y a un dispositivo
    user   = relationship("User", back_populates="loans")
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf
    device = relationship("Device", back_populates="loans")
