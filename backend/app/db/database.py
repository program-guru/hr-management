from sqlmodel import SQLModel, create_engine, Session

MYSQL_URL = "mysql://root:root@localhost:3306/hr_management_db"

# The engine is the core interface to the database
engine = create_engine(MYSQL_URL, echo=True)

# Initialize the database by creating all tables defined in our SQLModel models
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency function to get a database session
def get_session():
    with Session(engine) as session:
        yield session