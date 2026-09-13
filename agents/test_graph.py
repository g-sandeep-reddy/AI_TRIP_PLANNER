from backend.models import TripRequest
from agents.graph import graph


trip = TripRequest(
    destination="Kerala",
    days=3,
    budget=10000,
    interests=["nature", "adventure"]
)


result = graph.invoke({
    "trip": trip
})


print("\nFINAL STATE:")
print(result)