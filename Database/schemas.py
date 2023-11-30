from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    name: str
    unq_id: int
    position: float
    status: Optional[bool] = True
