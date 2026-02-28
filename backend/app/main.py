from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.db.database import create_db_and_tables
from app.api.routers import auth, employees
from app.models.dto import DTO

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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=DTO(
            success=False,
            message="Validation error",
            data=exc.errors()
        ).model_dump()
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=DTO(
            success=False,
            message="Internal server error",
            data=str(exc)
        ).model_dump()
    )

# Register our authentication router
app.include_router(auth.router)
app.include_router(employees.router)