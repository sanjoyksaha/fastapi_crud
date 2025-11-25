from datetime import datetime
from xmlrpc.client import DateTime

from sqlalchemy import Boolean, Column, Integer, String, Double, ForeignKey
from sqlalchemy.orm import relationship

from Database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    unq_id = Column(String, unique=True)
    position_x = Column(Double)
    position_y = Column(Double)
    status = Column(Boolean, default=True)
    is_superadmin = Column(Integer, default=0)

    jobs = relationship('Jobs', back_populates='creator')


class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    unq_id = Column(Integer, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    position_x = Column(Double)
    position_y = Column(Double)
    status = Column(Integer, default=1)
    door_open = Column(Integer, default=0)
    creator = relationship('User', back_populates='jobs')


class UserTokens(Base):
    __tablename__ = "user_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(String, unique=True)
    expired_at = Column(Integer)
    status = Column(Integer, default=1)
