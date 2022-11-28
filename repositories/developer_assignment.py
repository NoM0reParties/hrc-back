from typing import Optional

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db import get_session
from models.developer_models.developer_assignment import DeveloperAssignment
from schemas.developer_assignment import DeveloperAssignmentCreateDTO


class DeveloperAssignmentRepository:
    db: AsyncSession

    def __init__(
        self, db: AsyncSession = Depends(get_session)
    ) -> None:
        self.db = db

    async def create(self, assignment: DeveloperAssignmentCreateDTO) -> None:
        values: dict = assignment.dict()
        await self.db.execute(insert(DeveloperAssignment).values(**values))
        await self.db.commit()

    async def find_existing_assignment(self, assignment: DeveloperAssignmentCreateDTO) -> Optional[DeveloperAssignment]:
        result = await self.db.execute(select(DeveloperAssignment).where(
            DeveloperAssignment.developer_id == assignment.developer_id,
            DeveloperAssignment.feature_team_order_id == assignment.feature_team_order_id,
        ))
        return result.scalar()

    async def delete(self, dev_assignment_id: int) -> None:
        await self.db.execute(
            delete(DeveloperAssignment).where(DeveloperAssignment.id == dev_assignment_id)
        )
        await self.db.commit()
