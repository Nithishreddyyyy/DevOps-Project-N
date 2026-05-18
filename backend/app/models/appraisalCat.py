from pydantic import BaseModel
from typing import Optional

class Criteria(BaseModel):
    category : str
    name : str
    weight : float
    is_active : Optional[bool] = True

