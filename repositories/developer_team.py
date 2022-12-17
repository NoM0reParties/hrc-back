from datetime import date
from typing import List, Optional, Tuple

from fastapi import Depends
from sqlalchemy import select, update, delete, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db import get_session
from mappers.developer_team_router import dev_team_list_mapper, team_list_mapper
from models import DeveloperTeam, Feature, FeatureTeamOrder, Sprint
from models.developer_models.developer import Developer
from models.developer_models.developer_assignment import DeveloperAssignment
from schemas import DevTeamBaseDTO
from schemas.developer_team import DevTeamBySprintDTO, DevTeamWithDevelopersDTO


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
    ) -> List[DevTeamWithDevelopersDTO]:
        result = await self.db.execute(select(
            Developer.id,
            Developer.first_name,
            Developer.last_name,
            Developer.involvement,
            Developer.dev_team_id,
            DeveloperTeam.id,
            DeveloperTeam.name,
        ).join(
            Developer, Developer.dev_team_id == DeveloperTeam.id, isouter=True
        ).order_by(
            DeveloperTeam.id.asc()
        ).offset(offset).limit(limit))
        return team_list_mapper(result.all())

    async def list_by_sprint(
            self,
            sprint_id: int,
            limit: Optional[int] = 20,
            offset: Optional[int] = 0,
    ) -> List[DevTeamBySprintDTO]:
        inner_stmt = select(
            FeatureTeamOrder.hours,
            DeveloperAssignment.developer_id,
            Sprint.beginning_date,
            Sprint.ending_date,
        ).join(
            Feature, FeatureTeamOrder.feature_id == Feature.id, isouter=True
        ).join(
            DeveloperAssignment, DeveloperAssignment.feature_team_order_id == FeatureTeamOrder.id
        ).join(
            Sprint, Feature.sprint_id == Sprint.id
        ).where(
            Feature.sprint_id == sprint_id
        ).subquery()
        sprint_hours_stmt = select(
            Sprint.beginning_date,
            Sprint.ending_date,
        ).where(Sprint.id == sprint_id).subquery()
        fto_count_stmt = select(
            func.count(FeatureTeamOrder.id).label("fto_count"),
            FeatureTeamOrder.dev_team_id.label("dt_id"),
        ).group_by(FeatureTeamOrder.dev_team_id).subquery()
        developers_stmt = select(
            Developer.id.label('dev_id'),
            Developer.first_name,
            Developer.last_name,
            Developer.involvement,
            DeveloperTeam.id.label('dt_id'),
            func.sum(inner_stmt.c.hours).label('fto_load'),
            func.count(inner_stmt.c.hours).label('fto_assigned'),
            sprint_hours_stmt.c.beginning_date,
            sprint_hours_stmt.c.ending_date,
            fto_count_stmt.c.fto_count,
        ).join(
            DeveloperTeam, Developer.dev_team_id == DeveloperTeam.id, isouter=True
        ).join(
            fto_count_stmt, fto_count_stmt.c.dt_id == DeveloperTeam.id
        ).join(
            sprint_hours_stmt, 1 == 1
        ).join(inner_stmt, inner_stmt.c.developer_id == Developer.id, isouter=True).group_by(
            Developer.id, DeveloperTeam.id, DeveloperTeam.name, sprint_hours_stmt.c.beginning_date,
            sprint_hours_stmt.c.ending_date, fto_count_stmt.c.fto_count
        ).subquery()
        result = await self.db.execute(
            select(
                developers_stmt.c.dev_id,
                developers_stmt.c.first_name,
                developers_stmt.c.last_name,
                developers_stmt.c.involvement,
                DeveloperTeam.id,
                DeveloperTeam.name,
                developers_stmt.c.fto_load,
                developers_stmt.c.fto_assigned,
                developers_stmt.c.beginning_date,
                developers_stmt.c.ending_date,
                developers_stmt.c.fto_count,
            ).join(
                developers_stmt, developers_stmt.c.dt_id == DeveloperTeam.id, isouter=True
            )
        )
        return dev_team_list_mapper(result.all())

    async def get(self, dev_team_id: int) -> DeveloperTeam:
        result = await self.db.execute(select(DeveloperTeam).where(DeveloperTeam.id == dev_team_id))
        return result.scalar()

    async def create(self, dev_team: DevTeamBaseDTO):
        values: dict = dev_team.dict()
        await self.db.execute(insert(DeveloperTeam).values(**values))
        await self.db.commit()

    async def update(self, dev_team_id: int, dev_team: DevTeamBaseDTO):
        values: dict = dev_team.dict()
        await self.db.execute(update(DeveloperTeam).where(DeveloperTeam.id == dev_team_id).values(**values))
        await self.db.commit()

    async def delete(self, dev_team_id: int) -> None:
        await self.db.execute(
            delete(DeveloperTeam).where(DeveloperTeam.id == dev_team_id)
        )
        await self.db.commit()
