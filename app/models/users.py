from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP

class User(Base) :
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    role = Column(String, nullable = False)

    created_at = Column(
        TIMESTAMP(timezone = True), 
        nullable = False, 
        server_default = text('now()')
    )