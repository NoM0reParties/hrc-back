from pydantic import BaseModel

from schemas.developer_team import DevTeamDTO


class DeveloperCreateDTO(BaseModel):
    first_name: str
    last_name: str
    involvement: int
    dev_team_id: int


class DeveloperDTO(BaseModel):
    id: int
    name: str
    involvement: int
    dev_team_id: int


class DeveloperWithTeamDTO(DeveloperDTO):
    dev_team: DevTeamDTO
