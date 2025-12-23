from pydantic import BaseModel
from typing import Optional

class UserVisit(BaseModel):
    ip: str
    city: Optional[str]
    region: Optional[str]
    postal: Optional[str]
    country: Optional[str]
    timezone: Optional[str]
    org: Optional[str]
    path: str 
    user_agent: Optional[str]
