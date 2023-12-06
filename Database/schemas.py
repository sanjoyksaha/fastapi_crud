from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    name: str
    unq_id: int
    position_x: float
    position_y: float
    status: Optional[bool] = True


class Jobs(BaseModel):
    unq_id: Optional[int] = None
    user_id: int
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    status: int = 1

