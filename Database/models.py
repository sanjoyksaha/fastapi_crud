from sqlalchemy import Boolean, Column, Integer, String, Double
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    unq_id = Column(String, unique=True)
    position = Column(Double)
    status = Column(Boolean, default=True)
