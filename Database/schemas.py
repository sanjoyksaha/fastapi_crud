from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    name: str
    unq_id: int
    position_x: float
    position_y: float
    status: Optional[bool] = True


class Jobs(BaseModel):
    unq_id: int
    user_id: int
    position_x: float
    position_y: float
    status: int = 1
