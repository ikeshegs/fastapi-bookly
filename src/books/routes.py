from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.schemas import Book, BookUpdateModel
from src.books.models import Book
from src.books.service import BookService
from src.db.main import get_session

book_router = APIRouter()
book_service = BookService()

@book_router.get("/")
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = book_service.get_all_books(session)
    return books
