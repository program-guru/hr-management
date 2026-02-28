from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.database import create_db_and_tables
from app.api.routers import auth

# The lifespan context manager handles startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs when the server starts
    print("Starting up... creating database tables.")
    create_db_and_tables()
    yield
    # Anything after 'yield' runs when the server shuts down
    print("Shutting down...")

app = FastAPI(
    title="HRConnect API",
    description="Backend for the HRConnect Human Resource Management System",
    lifespan=lifespan
)

# Register our authentication router
app.include_router(auth.router)