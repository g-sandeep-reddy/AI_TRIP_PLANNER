# 🤖 AI Trip Planner

### Agentic AI Travel Planning Platform

An end-to-end **Agentic AI travel planning application** that combines **Gemini, LangGraph, RAG, real-time weather data, FastAPI, PostgreSQL, JWT authentication, and Streamlit** to generate personalized and practical travel itineraries.

🌐 **Live Application:** https://ai-trip-planner-frontend-c2py.onrender.com

📦 **GitHub Repository:** https://github.com/g-sandeep-reddy/AI_TRIP_PLANNER

---

## 🚀 Overview

Traditional travel applications often provide static recommendations.

**AI Trip Planner** uses an Agentic AI workflow to dynamically combine:

- User preferences
- Destination-specific knowledge
- Retrieved information through RAG
- Real-time weather conditions
- Budget constraints
- LLM-based reasoning

The system takes a user's:

- 📍 Destination
- 📅 Number of days
- 💰 Budget
- ❤️ Interests

and generates a structured, personalized **day-by-day travel itinerary**.

The application also supports user authentication, persistent trip history, and conversational travel assistance.

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │        USER          │
                         │                      │
                         │ Destination          │
                         │ Days                 │
                         │ Budget               │
                         │ Interests            │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Streamlit Frontend   │
                         │                      │
                         │ Trip Planner         │
                         │ Chat                 │
                         │ My Trips             │
                         │ Weather              │
                         └──────────┬───────────┘
                                    │
                              REST API
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   FastAPI Backend    │
                         │                      │
                         │ JWT Authentication   │
                         │ API Endpoints        │
                         │ Request Validation   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                 ┌─────────────────────────────────────┐
                 │          LangGraph Workflow         │
                 │                                     │
                 │  State-driven Agentic AI Pipeline   │
                 └──────────────────┬──────────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────┐
                    │       Research Agent        │
                    │                             │
                    │          Gemini             │
                    └──────────────┬──────────────┘
                                   │
                              RAG Query
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │     Gemini Embeddings       │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │          ChromaDB            │
                    │                             │
                    │   Travel Knowledge Base     │
                    └──────────────┬──────────────┘
                                   │
                         Relevant Knowledge
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │        Weather Tool         │
                    │                             │
                    │       Open-Meteo API        │
                    └──────────────┬──────────────┘
                                   │
                            Weather Data
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │      Itinerary Agent        │
                    │                             │
                    │          Gemini             │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │       Structured TripPlan   │
                    │                             │
                    │ Days • Activities • Budget │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │         PostgreSQL          │
                    │                             │
                    │ Users • Trips • Chat History│
                    └─────────────────────────────┘
