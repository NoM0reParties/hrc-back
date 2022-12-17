from typing import List, Optional

from pydantic import BaseModel


class DevTeamBaseDTO(BaseModel):
    name: str


class DevTeamDTO(DevTeamBaseDTO):
    id: int


class DeveloperDTO(BaseModel):
    id: int
    first_name: str
    last_name: str
    involvement: int
    dev_team_id: Optional[int]

class DevTeamWithDevelopersDTO(DevTeamDTO):
    developers: List[DeveloperDTO]


class DeveloperBySprintDTO(DeveloperDTO):
    sprint_load: Optional[int] = 0
    possible_hours: int
    fto_count: int


class DevTeamBySprintDTO(DevTeamBaseDTO):
    id: int
    name: str
    developers: List[DeveloperBySprintDTO]
    team_load: int
    team_load_overall: int
    fto_overall: int
    fto_assigned: int
