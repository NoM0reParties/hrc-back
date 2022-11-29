from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db import get_session
from models import Sprint
from schemas import SprintBaseDTO


class SprintRepository:
    db: AsyncSession

    def __init__(
        self, db: AsyncSession = Depends(get_session)
    ) -> None:
        self.db = db

    async def list(
        self,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
    ) -> List[Sprint]:
        result = await self.db.execute(select(Sprint).order_by(Sprint.id.desc()).offset(offset).limit(limit))
        return result.scalars().all()

    async def get(self, sprint_id: int) -> Sprint:
        result = await self.db.execute(select(Sprint).where(Sprint.id == sprint_id))
        return result.scalar()

    async def create(self, sprint: SprintBaseDTO) -> Sprint:
        values: dict = sprint.dict()
        new_sprint: Sprint = await self.db.execute(
            insert(Sprint).values(**values).execution_options(synchronize_session="fetch").returning(
                Sprint.id, Sprint.name, Sprint.ending_date, Sprint.beginning_date, Sprint.gap,
            ),
        )
        await self.db.commit()
        return new_sprint.fetchone()

    async def update(self, sprint_id: int, sprint: SprintBaseDTO) -> None:
        values: dict = sprint.dict()
        new_sprint: Sprint = await self.db.execute(
            update(Sprint).where(Sprint.id == sprint_id).values(
                **values).execution_options(synchronize_session="fetch")
        )
        await self.db.commit()
        return new_sprint.fetchone()

    async def delete(self, sprint_id: int) -> None:
        await self.db.execute(
            delete(Sprint).where(Sprint.id == sprint_id)
        )
        await self.db.commit()
