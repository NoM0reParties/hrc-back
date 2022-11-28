from typing import List

from pydantic import BaseModel

from schemas.feature_team_order import FeatureTeamOrderDTO


class FeatureDTO(BaseModel):
    id: int
    name: str
    dev_team_orders: List[FeatureTeamOrderDTO]


class FeatureBaseDTO(BaseModel):
    name: str
    sprint_id: int


class FeatureResponseDTO(FeatureBaseDTO):
    id: int
