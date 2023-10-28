from typing import List, Dict
from datetime import datetime
from pydantic import BaseModel


class ParisDB(BaseModel):
    sport_id: str
    sport_name: str
    participating_country: list
    date_time: datetime
    result: dict

class Result(BaseModel):
    sport_id: str
    result: dict