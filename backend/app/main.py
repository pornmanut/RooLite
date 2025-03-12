from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .game import routes as game_routes

app = FastAPI(title="Tic-tac-toe API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include game routes
app.include_router(game_routes.router, prefix="/game", tags=["game"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Tic-tac-toe API is running"}
