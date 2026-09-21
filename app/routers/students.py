from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Student
from ..schemas import StudentCreate, StudentResponse, StudentUpdate

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    if db.query(Student).filter(Student.email == student.email).first():
        raise HTTPException(status_code=409, detail="A student with this email already exists")

    record = Student(**student.model_dump())
    db.add(record)
    try:
        db.commit()
        db.refresh(record)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A student with this email already exists")
    return record


@router.get("", response_model=list[StudentResponse])
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).order_by(Student.id).all()


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    record = db.query(Student).filter(Student.id == student_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    return record


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    record = db.query(Student).filter(Student.id == student_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")

    duplicate = (
        db.query(Student)
        .filter(Student.email == student.email, Student.id != student_id)
        .first()
    )
    if duplicate:
        raise HTTPException(status_code=409, detail="A student with this email already exists")

    for key, value in student.model_dump().items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    record = db.query(Student).filter(Student.id == student_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    db.delete(record)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
