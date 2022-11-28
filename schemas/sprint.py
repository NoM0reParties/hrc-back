from datetime import date, datetime

from pydantic import BaseModel, validator


class SprintBaseDTO(BaseModel):
    name: str
    beginning_date: date
    ending_date: date
    gap: int = 0

    @validator("beginning_date", "ending_date", pre=True)
    def parse_date(cls, value):
        if isinstance(value, str):
            return value.split('T')[0]
        return value


class SprintDTO(SprintBaseDTO):
    id: int
