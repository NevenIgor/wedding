from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GuestCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    will_attend: bool
    drink_preference: Optional[str] = None


class GuestResponse(BaseModel):
    id: int
    name: str
    will_attend: bool
    drink_preference: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class GuestListResponse(BaseModel):
    guests: list[GuestResponse]
    total: int


class StatsResponse(BaseModel):
    total_guests: int
    attending: int
    not_attending: int
