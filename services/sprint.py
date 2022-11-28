from typing import List, Optional

from fastapi import Depends

from models import Sprint
from repositories import SprintRepository
from schemas import SprintBaseDTO


class SprintService:
    repository: SprintRepository

    def __init__(
            self, repository: SprintRepository = Depends()
    ) -> None:
        self.repository = repository

    async def create(self, sprint: SprintBaseDTO) -> Sprint:
        return await self.repository.create(sprint)

    async def delete(self, sprint_id: int) -> None:
        return await self.repository.delete(sprint_id)

    async def get(self, sprint_id: int) -> Sprint:
        return await self.repository.get(sprint_id=sprint_id)

    async def list(
            self,
            limit: Optional[int] = 20,
            offset: Optional[int] = 0,
    ) -> List[Sprint]:
        return await self.repository.list(
            limit=limit,
            offset=offset,
        )

    async def update(
        self, sprint_id: int, sprint: SprintBaseDTO
    ) -> None:
        return await self.repository.update(
            sprint_id, sprint
        )
