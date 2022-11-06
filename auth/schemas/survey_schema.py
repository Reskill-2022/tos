import datetime

from pydantic import BaseModel 
from typing import Optional, Dict



class Survey(BaseModel):
    email: str
    data: Dict
    created_at: Optional[datetime.datetime] = datetime.datetime.now()
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()