from symtable import Class
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    name: str
    unq_id: Optional[int] = 0
    position_x: float
    position_y: float
    status: Optional[bool] = True
    is_superuser: Optional[int] = 0


class Jobs(BaseModel):
    unq_id: Optional[int] = None
    user_id: int
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    status: int = 1
    door_open: Optional[int]= 0

class JobStatus(BaseModel):
    status: int

class DoorStatus(BaseModel):
    door_open: int


class Authentication(BaseModel):
    userid: str
    # password: str

class UserTokens(BaseModel):
    user_id: int
    token: str
    expired_at: int
    status: int