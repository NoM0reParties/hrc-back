from pydantic import BaseModel


class DevTeamBaseDTO(BaseModel):
    name: str


class DevTeamDTO(DevTeamBaseDTO):
    id: int
