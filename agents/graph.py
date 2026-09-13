from langgraph.graph import StateGraph, START, END

from agents.state import TripState
from agents.nodes import (
    research_agent,
    get_weather_node,
    itinerary_agent
)


graph_builder = StateGraph(TripState)


graph_builder.add_node("research", research_agent)
graph_builder.add_node("get_weather", get_weather_node)
graph_builder.add_node("itinerary", itinerary_agent)


graph_builder.add_edge(START, "research")
graph_builder.add_edge("research", "get_weather")
graph_builder.add_edge("get_weather", "itinerary")
graph_builder.add_edge("itinerary", END)


graph = graph_builder.compile()