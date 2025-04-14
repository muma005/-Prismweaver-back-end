
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
from app.utils.logging import logger

app = FastAPI(title="Prismweaver Backend")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info("Prismweaver backend started")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Prismweaver backend shut down")