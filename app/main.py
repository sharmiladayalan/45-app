from contextlib import asynccontextmanager

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.database.session import create_db_tables

from app.api.router import router

# Now our database is ready with async support when the app starts, 
# and we can use async sessions in our endpoints

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_db_tables()
    yield

# FastAPI App
app = FastAPI(
    # Server start/stop listener
    lifespan=lifespan_handler,
)

app.include_router(router)

### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
