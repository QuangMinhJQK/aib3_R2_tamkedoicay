from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from backend.app.api.endpoints import users, appointments, metrics, ai, notifications, video
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="CareLoop API",
    description="Backend API for CareLoop Healthcare App",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(users.router)
app.include_router(appointments.router)
app.include_router(metrics.router)
app.include_router(ai.router)
app.include_router(notifications.router)
app.include_router(video.router, prefix="/api/v1/videos", tags=["Videos"])

# Mount static directory for videos
app.mount("/static/videos", StaticFiles(directory="output"), name="videos")


@app.get("/")
async def root():
    return {"message": "Welcome to CareLoop API", "status": "online"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
