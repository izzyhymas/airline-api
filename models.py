from pydantic import BaseModel
from enum import Enum


class Flight(BaseModel):
    flight_num: str
    capacity: int
    estimated_flight_duration: int

class AirlineName(Enum):
    DELTA = "Delta"
    SOUTHWEST = "Southwest"
    ALASKA = "Alaska"