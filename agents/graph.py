from langgraph.graph import StateGraph, START, END

from agents.state import TripState
from agents.nodes import (
    planner_agent,
    research_agent,
    get_weather_node,
    itinerary_agent,
    reviewer_agent
)


graph_builder = StateGraph(TripState)


graph_builder.add_node("planner", planner_agent)
graph_builder.add_node("research", research_agent)
graph_builder.add_node("get_weather", get_weather_node)
graph_builder.add_node("itinerary", itinerary_agent)
graph_builder.add_node("reviewer", reviewer_agent)


graph_builder.add_edge(START, "planner")
graph_builder.add_edge("planner", "research")
graph_builder.add_edge("research", "get_weather")
graph_builder.add_edge("get_weather", "itinerary")
graph_builder.add_edge("itinerary", "reviewer")


def review_router(state: TripState):

    review = state["review"]
    attempts = state.get("review_attempts", 0)

    if review.approved:
        return "approved"

    if attempts >= 3:
        return "approved"

    return "replan"


graph_builder.add_conditional_edges(
    "reviewer",
    review_router,
    {
        "approved": END,
        "replan": "itinerary"
    }
)


graph = graph_builder.compile()