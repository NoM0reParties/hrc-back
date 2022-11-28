from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db import get_session
from models import FeatureTeamOrder
from schemas import FeatureTeamOrderBaseDTO
from schemas.feature_team_order import FeatureTeamOrderUpdateDTO


class FeatureTeamOrderRepository:
    db: AsyncSession

    def __init__(
            self, db: AsyncSession = Depends(get_session)
    ) -> None:
        self.db = db

    async def list(
            self,
            limit: Optional[int] = 20,
            offset: Optional[int] = 0,
    ) -> List[FeatureTeamOrder]:
        result = await self.db.execute(select(FeatureTeamOrder).order_by(
            FeatureTeamOrder.id.desc()).offset(offset).limit(limit))
        return result.scalars().all()

    async def get(self, order_id: int) -> FeatureTeamOrder:
        result = await self.db.execute(select(FeatureTeamOrder).where(FeatureTeamOrder.id == order_id))
        return result.scalar()

    async def create(self, order: FeatureTeamOrderUpdateDTO) -> int:
        values: dict = order.dict()
        del values['developer_id']
        result = await self.db.execute(insert(FeatureTeamOrder).values(**values).returning(FeatureTeamOrder.id))
        new_id = result.fetchone()
        await self.db.commit()
        return new_id[0]

    async def update(self, order_id: int, order: FeatureTeamOrderUpdateDTO) -> None:
        values: dict = order.dict()
        del values['developer_id']
        del values['feature_id']
        await self.db.execute(update(FeatureTeamOrder).where(FeatureTeamOrder.id == order_id).values(**values))
        await self.db.commit()

    async def delete(self, order_id: int) -> None:
        await self.db.execute(delete(FeatureTeamOrder).where(FeatureTeamOrder.id == order_id))
        await self.db.commit()
