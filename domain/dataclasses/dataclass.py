from datetime import datetime, date
from typing import Optional

from dataclasses import dataclass


@dataclass
class User:
    phone: str
    fam: str
    name: str
    id: Optional[int] = None
    email: Optional[str] = None
    otc: Optional[str] = None


@dataclass
class Coords:
    latitude: float
    longitude: float
    height: int
    id: Optional[int] = None


@dataclass
class Level:
    winter: str
    summer: str
    autumn: str
    spring: str
    id: Optional[int] = None


@dataclass
class Image:
    img: str
    title: str
    pereval_id: int
    date_added: date
    id: Optional[int] = None


@dataclass
class PerevalAdded:
    date_added: Optional[date]
    beauty_title: str
    title: str
    other_titles: str
    connect: str
    add_time: datetime
    user_id: int
    coords_id: int
    level_id: int
    id: Optional[int] = None
    status: Optional[bool] = False
