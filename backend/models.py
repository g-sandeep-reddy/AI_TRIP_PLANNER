from pydantic import BaseModel
from typing import List


class TripRequest(BaseModel):

    destination: str
    days: int
    budget: int
    interests: List[str]


class Activity(BaseModel):

    time: str
    activity: str
    description: str


class DayPlan(BaseModel):

    day: int
    title: str
    activities: List[Activity]


class TripPlan(BaseModel):

    destination: str
    summary: str
    estimated_budget: int
    days: List[DayPlan]


class WeatherData(BaseModel):

    temperature: float
    humidity: int
    weather_code: int
    wind_speed: float


class RegisterRequest(BaseModel):

    username: str
    email: str
    password: str


class LoginRequest(BaseModel):

    username: str
    password: str


class ChatMessageRequest(BaseModel):

    session_id: int
    message: str