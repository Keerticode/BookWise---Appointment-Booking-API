from .database import Base
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Appointments(Base) :
    __tablename__ = "appointments"

    id = Column(Integer, primary_key = True, nullable = False)
    customer_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    slot_id = Column(Integer, ForeignKey("availability_slots.id", ondelete = "CASCADE"), nullable = False)

    status = Column(String, nullable = False, server_default=text("'booked'"))

    created_at = Column(
        TIMESTAMP(timezone = True),
        nullable = False,
        server_default = text("now()")
    )

    updated_at = Column(
        TIMESTAMP(timezone = True),
        nullable = False,
        server_default = text("now()"),
        onupdate = func.now() 
    )

    customer = relationship("User")
    slot = relationship("AvailabilitySlot")