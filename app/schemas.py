from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    department: str = Field(..., min_length=2, max_length=100)
    year: int = Field(..., ge=1, le=4)
    cgpa: float = Field(..., ge=0, le=10)

    @field_validator("name", "department")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
