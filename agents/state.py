from typing import TypedDict

from backend.models import TripRequest, WeatherData, TripPlan


class TripState(TypedDict, total=False):

    trip: TripRequest

    research: str

    weather: WeatherData

    trip_plan: TripPlan