from sqlmodel import SQLModel, create_engine, Session

from app.core.config import settings

# The engine is the core interface to the database
engine = create_engine(settings.DATABASE_URI, echo=True)

# Initialize the database by creating all tables defined in our SQLModel models
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency function to get a database session
def get_session():
    with Session(engine) as session:
        yield session