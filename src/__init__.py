from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router

from src.db.main import init_db

from .errors import register_all_errors
from .middleware import register_middleware


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Server is starting ... ")
    await init_db()
    yield
    print(f"Server has been stopped")

version = "v1"

app = FastAPI(
    title = "Bookly",
    description = "A Rest API for a book review web service",
    version = version,
    # lifespan = life_span # Removed since I'm using Alembic
)

register_all_errors(app)

register_middleware(app)


app.include_router(book_router, prefix=f"/api/{version}/book", tags=["Book"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
app.include_router(review_router, prefix=f"/api/{version}/review", tags=["Review"])
app.include_router(tags_router, prefix=f"/api/{version}/tag", tags=["Tag"])
