from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.strategy_options import contains_eager

from configs.db import get_session
from mappers.feature_router import feature_list_mapper
from models import Feature, FeatureTeamOrder
from models.developer_models.developer import Developer
from models.developer_models.developer_assignment import DeveloperAssignment
from models.developer_models.developer_team import DeveloperTeam
from schemas import FeatureBaseDTO, FeatureDTO


class FeatureRepository:
    db: AsyncSession

    def __init__(
            self, db: AsyncSession = Depends(get_session)
    ) -> None:
        self.db = db

    async def list_by_sprint(self, sprint_id: int) -> List[FeatureDTO]:
        result = await self.db.execute(
            select(FeatureTeamOrder, Feature, Developer, DeveloperTeam, DeveloperAssignment).join(
                Feature, FeatureTeamOrder.feature_id == Feature.id, isouter=True).join(
                DeveloperAssignment, FeatureTeamOrder.id == DeveloperAssignment.feature_team_order_id, isouter=True).join(
                DeveloperTeam, FeatureTeamOrder.dev_team_id == DeveloperTeam.id, isouter=True).join(
                Developer, DeveloperAssignment.developer_id == Developer.id, isouter=True).where(
                Feature.sprint_id == sprint_id).order_by(Feature.id.desc())
        )
        return feature_list_mapper(result.all())

    async def get(self, feature_id: int) -> Feature:
        result = await self.db.execute(
            select(Feature).where(Feature.id == feature_id)
        )
        return result.scalar()

    async def list(
            self,
            limit: Optional[int] = 20,
            offset: Optional[int] = 0,
    ) -> Feature:
        result = await self.db.execute(
            select(Feature).order_by(Feature.id.desc()).offset(offset).limit(limit)
        )
        return result.scalars().all()

    async def create(self, feature: FeatureBaseDTO) -> Feature:
        values: dict = feature.dict()
        new_feature: Feature = await self.db.execute(
            insert(Feature).values(**values).execution_options(synchronize_session="fetch").returning(
                Feature.id, Feature.name, Feature.sprint_id
            ),
        )
        await self.db.commit()
        return new_feature.fetchone()

    async def update(self, feature_id: int, feature: FeatureBaseDTO) -> None:
        values: dict = feature.dict()
        await self.db.execute(
            update(Feature).where(Feature.id == feature_id).values(
                **values).execution_options(synchronize_session="fetch")
        )
        await self.db.commit()

    async def delete(self, feature_id: int) -> None:
        await self.db.execute(delete(Feature).where(Feature.id == feature_id))
        await self.db.commit()
