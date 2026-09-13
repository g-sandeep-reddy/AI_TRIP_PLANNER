import os

from dotenv import load_dotenv
from google import genai

from agents.state import TripState
from backend.models import TripPlan

from tools.weather import get_weather

from rag.retrieve import retrieve_documents


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def parse_trip(state: TripState):

    trip = state["trip"]

    return {
        "trip": trip
    }


def get_weather_node(state: TripState):

    weather = get_weather(10.0889, 77.0595)

    return {
        "weather": weather
    }


def research_agent(state: TripState):

    trip = state["trip"]

    query = f"""
    Destination: {trip.destination}
    Interests: {", ".join(trip.interests)}
    Budget: {trip.budget}
    """

    results = retrieve_documents(query)

    documents = results["documents"][0]

    knowledge = "\n\n".join(documents)

    prompt = f"""
    Research the destination based on the travel request.

    Destination: {trip.destination}
    Number of days: {trip.days}
    Budget: {trip.budget}
    Interests: {", ".join(trip.interests)}

    Relevant travel knowledge:
    {knowledge}

    Use the relevant travel knowledge to create useful research.

    Focus on:
    - Important places to visit
    - Activities
    - Nature or adventure opportunities
    - Budget considerations
    - Travel considerations

    Return concise research information.
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    research = response.text

    return {
        "research": research
    }


def itinerary_agent(state: TripState):

    trip = state["trip"]
    weather = state["weather"]
    research = state["research"]

    prompt = f"""
    Create a practical day-by-day travel itinerary.

    Trip request:
    Destination: {trip.destination}
    Number of days: {trip.days}
    Budget: {trip.budget}
    Interests: {", ".join(trip.interests)}

    Weather:
    Temperature: {weather.temperature}°C
    Humidity: {weather.humidity}%
    Weather code: {weather.weather_code}
    Wind speed: {weather.wind_speed} km/h

    Destination research:
    {research}

    Use the destination research and weather information
    to create a realistic itinerary.

    Requirements:
    - The destination field must exactly match the destination provided in the trip request.
    - Follow the user's interests.
    - Consider the weather when selecting activities.
    - Avoid unrealistic travel schedules.
    - Include practical activities for each day.
    - Estimate the total trip cost.
    - The estimated total trip cost must be within the user's budget.
    - The estimated total cost must be returned in estimated_budget.
    - Do not exceed the requested budget.
    - Return a structured day-by-day itinerary.
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": TripPlan,
        }
    )

    trip_plan = response.parsed

    return {
        "trip_plan": trip_plan
    }