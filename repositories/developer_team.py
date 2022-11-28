from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db import get_session
from models import DeveloperTeam
from schemas import DevTeamBaseDTO


class DeveloperTeamRepository:
    db: AsyncSession

    def __init__(
        self, db: AsyncSession = Depends(get_session)
    ) -> None:
        self.db = db

    async def list(
        self,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
    ) -> List[DeveloperTeam]:
        result = await self.db.execute(select(DeveloperTeam).order_by(
            DeveloperTeam.id.desc()).offset(offset).limit(limit))
        return result.scalars().all()

    async def get(self, dev_team_id: int) -> DeveloperTeam:
        result = await self.db.execute(select(DeveloperTeam).where(DeveloperTeam.id == dev_team_id))
        return result.scalar()

    async def create(self, dev_team: DevTeamBaseDTO) -> DeveloperTeam:
        values: dict = dev_team.dict()
        new_dev: DeveloperTeam = await self.db.execute(
            insert(DeveloperTeam).values(**values).execution_options(synchronize_session="fetch").returning(
                DeveloperTeam.id, DeveloperTeam.first_name, DeveloperTeam.last_name, DeveloperTeam.involvement
            ),
        )
        await self.db.commit()
        return new_dev.fetchone()

    async def update(self, dev_team_id: int, dev_team: DevTeamBaseDTO) -> DeveloperTeam:
        values: dict = dev_team.dict()
        new_dev: DeveloperTeam = await self.db.execute(
            update(DeveloperTeam).where(DeveloperTeam.id == dev_team_id).values(
                **values).execution_options(synchronize_session="fetch").returning(
                DeveloperTeam.id, DeveloperTeam.first_name, DeveloperTeam.last_name, DeveloperTeam.involvement
            ),
        )
        await self.db.commit()
        return new_dev.fetchone()

    async def delete(self, dev_team_id: int) -> None:
        await self.db.execute(
            delete(DeveloperTeam).where(DeveloperTeam.id == dev_team_id)
        )
        await self.db.commit()
