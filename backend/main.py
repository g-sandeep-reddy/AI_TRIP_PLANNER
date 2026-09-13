import os
import json
from dotenv import load_dotenv
from google import genai
from agents.graph import graph


from tools.weather import get_weather
from backend.models import (
    TripRequest,
    RegisterRequest,
    LoginRequest,
    ChatMessageRequest
)
from database.connection import SessionLocal, engine, Base
from database.models import User, Trip, ChatSession, ChatMessage
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.auth import hash_password, verify_password, create_access_token, verify_token


load_dotenv()

app = FastAPI()
Base.metadata.create_all(bind=engine)
security = HTTPBearer()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


@app.get("/")
def home():
    return {"message": "AI Trip Planner API is running"}


@app.post("/plan-trip")
def plan_trip(
    trip: TripRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    username = verify_token(token)

    result = graph.invoke({
        "trip": trip
    })

    db = SessionLocal()

    saved_trip = Trip(
        username=username,
        destination=trip.destination,
        days=trip.days,
        budget=trip.budget,
        interests=",".join(trip.interests),
        trip_plan=json.dumps(
            result["trip_plan"].model_dump()
        )
    )

    db.add(saved_trip)
    db.commit()
    db.refresh(saved_trip)

    db.close()

    return {
        "username": username,
        "weather": result["weather"],
        "trip_plan": result["trip_plan"]
    }

@app.get("/test-weather")
def test_weather(destination: str):

    coordinates = {
        "andhra pradesh": (15.9129, 79.7400),
        "arunachal pradesh": (28.2180, 94.7278),
        "assam": (26.2006, 92.9376),
        "bihar": (25.0961, 85.3131),
        "chhattisgarh": (21.2787, 81.8661),
        "goa": (15.4909, 73.8278),
        "gujarat": (22.2587, 71.1924),
        "haryana": (29.0588, 76.0856),
        "himachal pradesh": (31.1048, 77.1734),
        "jharkhand": (23.6102, 85.2799),
        "karnataka": (15.3173, 75.7139),
        "kerala": (10.8505, 76.2711),
        "madhya pradesh": (22.9734, 78.6569),
        "maharashtra": (19.7515, 75.7139),
        "manipur": (24.6637, 93.9063),
        "meghalaya": (25.4670, 91.3662),
        "mizoram": (23.1645, 92.9376),
        "nagaland": (26.1584, 94.5624),
        "odisha": (20.9517, 85.0985),
        "punjab": (31.1471, 75.3412),
        "rajasthan": (27.0238, 74.2179),
        "sikkim": (27.5330, 88.5122),
        "tamil nadu": (11.1271, 78.6569),
        "telangana": (18.1124, 79.0193),
        "tripura": (23.9408, 91.9882),
        "uttar pradesh": (26.8467, 80.9462),
        "uttarakhand": (30.0668, 79.0193),
        "west bengal": (22.9868, 87.8550),
    }

    location = destination.lower().strip()

    if location not in coordinates:
        return {
            "message": "Weather for this location is not supported yet."
        }

    latitude, longitude = coordinates[location]

    weather = get_weather(
        latitude,
        longitude
    )

    return {
        "destination": destination,
        "weather": weather
    }

@app.post("/register")
def register(request: RegisterRequest):

    db = SessionLocal()

    hashed_password = hash_password(request.password)

    user = User(
        username=request.username,
        email=request.email,
        password_hash=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    db.close()

    return {
        "message": "User registered successfully!",
        "username": user.username,
        "email": user.email
    }

@app.post("/login")
def login(request: LoginRequest):

    db = SessionLocal()

    user = db.query(User).filter(
        User.username == request.username
    ).first()

    if user is None:
        db.close()
        return {
            "message": "Invalid username or password"
        }

    if not verify_password(request.password, user.password_hash):
        db.close()
        return {
            "message": "Invalid username or password"
        }

    token = create_access_token(user.username)

    db.close()

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/my-trips")
def get_my_trips(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    username = verify_token(token)

    db = SessionLocal()

    trips = db.query(Trip).filter(
        Trip.username == username
    ).all()

    db.close()

    return trips

@app.post("/chat/start")
def start_chat(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    username = verify_token(token)

    db = SessionLocal()

    chat = ChatSession(
        username=username,
        title="New Trip Chat"
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    db.close()

    return {
        "session_id": chat.id,
        "title": chat.title
    }


@app.post("/chat/message")
def chat_message(
    request: ChatMessageRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    username = verify_token(token)

    db = SessionLocal()

    chat = db.query(ChatSession).filter(
        ChatSession.id == request.session_id,
        ChatSession.username == username
    ).first()

    if chat is None:
        db.close()
        return {
            "message": "Chat session not found"
        }

    previous_messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == request.session_id
    ).order_by(
        ChatMessage.id.asc()
    ).all()

    conversation = []

    for message in previous_messages:
        conversation.append(
            f"{message.role}: {message.message}"
        )

    conversation.append(
        f"user: {request.message}"
    )

    prompt = "\n".join(conversation)

    user_message = ChatMessage(
        session_id=request.session_id,
        role="user",
        message=request.message
    )

    db.add(user_message)
    db.commit()

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    ai_response = response.text

    assistant_message = ChatMessage(
        session_id=request.session_id,
        role="assistant",
        message=ai_response
    )

    db.add(assistant_message)
    db.commit()

    db.close()

    return {
        "session_id": request.session_id,
        "response": ai_response
    }