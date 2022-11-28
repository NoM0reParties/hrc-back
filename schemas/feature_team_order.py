from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schemas.developer import DeveloperDTO
from schemas.developer_team import DevTeamDTO


class FeatureTeamOrderDTO(BaseModel):
    id: int
    dev_team: DevTeamDTO
    updated: datetime
    assigned: bool
    hours: int
    auto_assignment: Optional[bool]
    assigned_developer: Optional[DeveloperDTO]
    gap: int


class FeatureTeamOrderUpdateDTO(BaseModel):
    feature_id: Optional[int]
    dev_team_id: int
    updated: Optional[datetime] = datetime.now()
    hours: int
    gap: Optional[int] = 0
    developer_id: Optional[int]
    assigned: Optional[bool]
    auto_assignment: Optional[bool]


class FeatureTeamOrderBaseDTO(BaseModel):
    dev_team_id: int
    feature_id: int
    updated: datetime
    assigned: bool
    hours: int
    auto_assignment: Optional[bool]
    gap: int


class FeatureTeamOrderResponseDTO(FeatureTeamOrderBaseDTO):
    id: int
