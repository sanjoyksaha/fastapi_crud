from sqlalchemy import Boolean, Column, Integer, String, Double
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    unq_id = Column(String, unique=True)
    position_x = Column(Double)
    position_y = Column(Double)
    status = Column(Boolean, default=True)


class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    unq_id = Column(Integer, unique=True)
    user_id = Column(Integer)
    position_x = Column(Double)
    position_y = Column(Double)
    status = Column(Integer, default=1)
