from typing import Dict
from datetime import datetime
from pydantic import BaseModel


class ParisDB(BaseModel):
    sport_id: str
    sport_name: str
    participating_country: list
    date_time: datetime
    result: Dict[str,str]


