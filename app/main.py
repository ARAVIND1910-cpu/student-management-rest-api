from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import Base, SessionLocal, engine
from .models import Student
from .routers.students import router as students_router


SAMPLE_STUDENTS = [
    {
        "name": "Rahul Kumar",
        "email": "rahul.kumar@example.com",
        "department": "Computer Science",
        "year": 2,
        "cgpa": 8.4,
    },
    {
        "name": "Priya Sharma",
        "email": "priya.sharma@example.com",
        "department": "Electronics",
        "year": 3,
        "cgpa": 9.1,
    },
    {
        "name": "Vikram Singh",
        "email": "vikram.singh@example.com",
        "department": "Mechanical",
        "year": 1,
        "cgpa": 7.8,
    },
    {
        "name": "Ananya Patel",
        "email": "ananya.patel@example.com",
        "department": "Information Technology",
        "year": 4,
        "cgpa": 8.7,
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(Student).count() == 0:
            db.add_all([Student(**student) for student in SAMPLE_STUDENTS])
            db.commit()
    finally:
        db.close()

    yield


app = FastAPI(
    title="Student Management REST API",
    description="A FastAPI + SQLite CRUD API with validation, error handling, and automatic OpenAPI documentation.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(students_router)


@app.get("/", tags=["System"])
def root():
    return {
        "message": "Student Management REST API is running",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
        "health": "/health",
    }


@app.get("/health", tags=["System"])
def health():
    return {"status": "healthy", "service": "student-management-api"}
