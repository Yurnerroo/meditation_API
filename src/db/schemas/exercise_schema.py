from pydantic import BaseModel, Field
from pydantic.validators import datetime


class ExerciseBase(BaseModel):
    text: str = Field(min_length=3, max_length=1000)
    time: datetime
    photo: str | None = None
    owner: int


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(ExerciseBase):
    pass


class ExerciseRead(ExerciseBase):
    id: int

    class Config:
        orm_mode = True


class ExerciseReadResponse(ExerciseRead):
    pass

