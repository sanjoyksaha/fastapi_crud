from sqlalchemy import Boolean, Column, Integer, String, Double, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    unq_id = Column(String, unique=True)
    position_x = Column(Double)
    position_y = Column(Double)
    status = Column(Boolean, default=True)

    jobs = relationship('Jobs', back_populates='creator')


class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    unq_id = Column(Integer, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    position_x = Column(Double)
    position_y = Column(Double)
    status = Column(Integer, default=1)
    creator = relationship('User', back_populates='jobs')
