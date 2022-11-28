from typing import List, Optional
from fastapi import Depends

from models import Feature
from repositories import FeatureRepository
from schemas import FeatureBaseDTO, FeatureDTO


class FeatureService:
    repository: FeatureRepository

    def __init__(
            self, repository: FeatureRepository = Depends()
    ) -> None:
        self.repository = repository

    async def create(self, feature: FeatureBaseDTO) -> Feature:
        return await self.repository.create(feature)

    async def delete(self, feature_id: int) -> None:
        return await self.repository.delete(feature_id=feature_id)

    async def get(self, feature_id: int) -> Feature:
        return await self.repository.get(feature_id=feature_id)

    async def list_by_sprint(self, sprint_id: int) -> List[FeatureDTO]:
        return await self.repository.list_by_sprint(sprint_id=sprint_id)

    async def list(
            self,
            limit: Optional[int] = 20,
            offset: Optional[int] = 0,
    ) -> List[Feature]:
        return await self.repository.list(limit=limit, offset=offset)

    async def update(self, feature_id: int, feature: FeatureBaseDTO):
        await self.repository.update(
            feature_id=feature_id,
            feature=feature,
        )
