from .database import Base
from sqlalchemy import Integer, Column, String, Boolean, ForeignKey, text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Availabilities(Base) :

    __tablename__ = "availability_slots"

    id = Column(Integer, primary_key = True, nullable = False)
    service_id = Column(Integer, ForeignKey("services.id", ondelete = "CASCADE"), nullable = False)

    start_time = Column(
        TIMESTAMP(timezone = True),
        nullable = False,
        server_default = text('now()')
    )

    end_time = Column(
        TIMESTAMP(timezone = True),
        nullable = False,
        server_default = text('now()')
    )

    is_available = Column(Boolean, nullable = False)

    created_at = Column(
        TIMESTAMP(timezone = True),
        nullable = False,
        server_default = text('now()')
    )