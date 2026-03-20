from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(
    title="Book Management API",
    description="API dùng để quản lý sách (CRUD)",
    version="1.0.0",
)


# ===== Model =====
class Book(BaseModel):
    id: str = Field(..., example="1")
    title: str = Field(..., example="Clean Code")
    author: str = Field(..., example="Robert C. Martin")
    price: float = Field(..., gt=0, example=30)


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)


# ===== Fake Database =====
books = [
    {"id": "1", "title": "Clean Code", "author": "Robert C. Martin", "price": 30},
    {"id": "2", "title": "Atomic Habits", "author": "James Clear", "price": 25},
]


# ===== APIs =====


# GET ALL
@app.get("/api/books", response_model=List[Book])
def get_books():
    return books


# GET BY ID
@app.get("/api/books/{id}", response_model=Book)
def get_book(id: str):
    for b in books:
        if b["id"] == id:
            return b
    raise HTTPException(status_code=404, detail="Book not found")


# CREATE
@app.post("/api/books", response_model=Book, status_code=201)
def create_book(book: Book):
    # check duplicate ID
    for b in books:
        if b["id"] == book.id:
            raise HTTPException(status_code=400, detail="ID already exists")

    books.append(book.model_dump())
    return book


# UPDATE
@app.put("/api/books/{id}", response_model=Book)
def update_book(id: str, data: BookUpdate):
    for b in books:
        if b["id"] == id:
            update_data = data.model_dump(exclude_unset=True)
            b.update(update_data)
            return b
    raise HTTPException(status_code=404, detail="Book not found")


# DELETE
@app.delete("/api/books/{id}")
def delete_book(id: str):
    global books

    for b in books:
        if b["id"] == id:
            books = [book for book in books if book["id"] != id]
            return {"message": "Book deleted"}

    raise HTTPException(status_code=404, detail="Book not found")
