from typing import Dict
from datetime import datetime
from pydantic import BaseModel


class ParisDB(BaseModel):
    sport_id: str
    sport_name: str
    sport_type: str | None = None
    participating_country: list
    date_time: datetime
    result: Dict[str,list]
    
class Result(BaseModel):
    sport_id: str
    result: Dict[str,list]