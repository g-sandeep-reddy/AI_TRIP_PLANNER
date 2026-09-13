from typing import TypedDict

from backend.models import TripRequest, WeatherData, TripPlan, ReviewOutput


class TripState(TypedDict, total=False):
    trip: TripRequest
    plan: dict
    research: str
    weather: WeatherData
    trip_plan: TripPlan
    review: ReviewOutput
    review_attempts: int