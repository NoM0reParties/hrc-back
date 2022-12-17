from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db import get_session
from models import Developer
from schemas.developer import DeveloperCreateDTO


class DeveloperRepository:
    db: AsyncSession

    def __init__(
        self, db: AsyncSession = Depends(get_session)
    ) -> None:
        self.db = db

    async def list(
        self,
        team: Optional[int] = None,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
    ) -> List[Developer]:
        query = select(Developer)
        if team is not None:
            query = query.filter(Developer.dev_team_id == team)
        result = await self.db.execute(query.order_by(Developer.id.desc()).offset(offset).limit(limit))
        return result.scalars().all()

    async def get(self, developer_id: int) -> Developer:
        result = await self.db.execute(select(Developer).where(Developer.id == developer_id))
        return result.scalar()

    async def create(self, developer: DeveloperCreateDTO) -> None:
        values: dict = developer.dict()
        print(values)
        await self.db.execute(
            insert(Developer).values(**values).execution_options(synchronize_session="fetch")
        )
        await self.db.commit()

    async def update(self, developer_id: int, developer: DeveloperCreateDTO) -> None:
        values: dict = developer.dict()
        await self.db.execute(
            update(Developer).where(Developer.id == developer_id).values(
                **values)
        )
        await self.db.commit()

    async def delete(self, developer_id: int) -> None:
        await self.db.execute(
            delete(Developer).where(Developer.id == developer_id)
        )
        await self.db.commit()
