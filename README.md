# AI Trip Planner

An AI-powered travel planning application that generates personalized,
weather-aware travel itineraries using Gemini, LangGraph, RAG, external
tools, and PostgreSQL.

## Features

- Personalized trip planning
- Weather-aware recommendations
- Multi-agent architecture
- RAG-based destination research
- External tool integration
- Persistent trip and user data
- JWT authentication
- Trip evaluation

## Tech Stack

- Python
- FastAPI
- Gemini API
- LangChain
- LangGraph
- PostgreSQL
- RAG
- HTML/CSS/JavaScript
- Render

## Architecture

The application uses FastAPI as the backend API layer and LangGraph
to orchestrate multiple AI agents and external tools.

## Project Structure

```text
AI_TRIP_PLANNER/
├── backend/
├── frontend/
├── agents/
├── tools/
├── rag/
├── database/
├── evaluation/
├── knowledge/
├── .env
├── .gitignore
├── requirements.txt
└── README.md