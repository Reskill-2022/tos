import datetime

from pydantic import BaseModel 
from typing import Optional



class TOS(BaseModel):
    email: str
    tos_accepted: bool = False
    consent: bool = False
    created_at: Optional[datetime.datetime] = datetime.datetime.now()
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()