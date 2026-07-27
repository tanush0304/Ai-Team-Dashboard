from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# MUST be called before importing routes!
load_dotenv() 

from routes import ai, team, updates, projects
app = FastAPI(
    title="AI Team Dashboard API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://ai-team-dashboard.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(team.router)
app.include_router(updates.router)
app.include_router(ai.router)
app.include_router(projects.router)

@app.get("/")
def root():
    return {
        "message": "AI Team Dashboard API is running 🚀"
    }