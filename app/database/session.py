from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

# Create a database engine to connect with database
# It prepares how to connect to database
# "sqlite:///sqlite.db" → connects to a local SQLite database file named sqlite.db
# echo=True → Shows SQL queries in terminal
# connect_args → Special settings for SQLit
engine = create_engine(
    url="sqlite:///sqlite.db",
    echo=True,
    connect_args={"check_same_thread": False},
)

# This function creates database tables
# We import Shipment so SQLModel registers it
# If model is not imported → table will NOT be created
# metadata stores all models (tables)(SQLModel.metadata)
# create_all(engine) → creates tables inside sqlite.db
def create_db_tables():
    from app.schemas import Shipment  # noqa: F401
    SQLModel.metadata.create_all(bind=engine)


# Session to interact with database
# get_session() creates a database session
# Session is used to perform DB operations (insert, update, delete)
# "with" automatically closes session after use
# yield sends session to FastAPI route
def get_session():
    with Session(bind=engine) as session:
        yield session

# WITH Annotated
# We create reusable dependency type
# SessionDep stores Session + Depends(get_session)
SessionDep = Annotated[Session, Depends(get_session)]

# WITHOUT Annotated
# We directly use Depends(get_session) inside the route
# FastAPI calls get_session() and injects session automatically

''' @app.post("/example/")
def example_route(session: Session = Depends(get_session)):
    return {"message": "Using normal dependency"} '''