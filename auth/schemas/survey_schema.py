import datetime

from pydantic import BaseModel 
from typing import Optional, Dict



class Survey(BaseModel):
    email: str
    data: Dict
    created_at: datetime.datetime = datetime.datetime.utcnow()
    updated_at: datetime.datetime = datetime.datetime.utcnow()