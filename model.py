from typing import Dict
from datetime import datetime
from pydantic import BaseModel


class ParisDB(BaseModel):
    sport_id: str
    sport_name: str = None
    sport_type: str = None
    participating_country: list = None
    date_time: datetime = None
    result: Dict[str, list] = None


class Result(BaseModel):
    sport_id: str
    result: Dict[str, list] = None
