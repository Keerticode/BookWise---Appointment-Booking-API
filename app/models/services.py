from app.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Numeric, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Service(Base) :
    __tablename__ = "services"

    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String, nullable = False)
    description = Column(Text, nullable = False)
    duration_minutes = Column(Integer, nullable = False)
    price = Column(Numeric(10, 2), nullable = False)
    provider_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    created_at = Column(
        TIMESTAMP(timezone = True),
        nullable = False,
        server_default = text('now()')
    )