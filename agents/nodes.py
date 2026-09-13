import os

from dotenv import load_dotenv
from google import genai

from agents.state import TripState
from backend.models import TripPlan, PlannerOutput, ReviewOutput

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
    - Return the estimated total cost in estimated_budget.
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

def planner_agent(state: TripState):

    trip = state["trip"]

    prompt = f"""
    Analyze the following travel request and create a structured trip plan.

    Destination: {trip.destination}
    Number of days: {trip.days}
    Budget: {trip.budget}
    Interests: {", ".join(trip.interests)}

    Determine whether destination research is needed.
    Return only the structured planning information.
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": PlannerOutput,
        }
    )

    plan = response.parsed

    return {
        "plan": plan
    }

def research_agent(state: TripState):

    trip = state["trip"]
    plan = state["plan"]

    prompt = f"""
    Research the destination based on the travel request.

    Destination: {trip.destination}
    Number of days: {trip.days}
    Budget: {trip.budget}
    Interests: {", ".join(trip.interests)}

    Planner information:
    {plan}

    Identify useful destination information that can help
    another agent create a practical itinerary.

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

def research_agent(state: TripState):

    trip = state["trip"]
    plan = state["plan"]

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

    Planner information:
    {plan}

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


def reviewer_agent(state: TripState):

    trip = state["trip"]
    weather = state["weather"]
    trip_plan = state["trip_plan"]

    attempts = state.get("review_attempts", 0) + 1

    prompt = f"""
    Review the following travel itinerary.

    Trip requirements:
    Destination: {trip.destination}
    Number of days: {trip.days}
    Budget: {trip.budget}
    Interests: {", ".join(trip.interests)}

    Weather:
    Temperature: {weather.temperature}°C
    Humidity: {weather.humidity}%
    Weather code: {weather.weather_code}
    Wind speed: {weather.wind_speed} km/h

    Generated itinerary:
    {trip_plan}

    Evaluate the itinerary based on:

    1. Number of days
    2. User interests
    3. Budget
    4. Weather suitability
    5. Realistic travel schedule
    6. Overall usefulness

    Give a score from 0 to 100.

    Approve the itinerary if the score is 80 or higher.

    Return concise feedback explaining the decision.
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ReviewOutput,
        }
    )

    review = response.parsed

    return {
    "review": review,
    "review_attempts": attempts
}