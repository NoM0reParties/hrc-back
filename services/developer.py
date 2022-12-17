from typing import List, Optional
from fastapi import Depends

from models import Developer
from repositories import DeveloperRepository
from schemas import DeveloperCreateDTO


class DeveloperService:
    repository: DeveloperRepository

    def __init__(
            self, repository: DeveloperRepository = Depends()
    ) -> None:
        self.repository = repository

    async def create(self, developer: DeveloperCreateDTO) -> None:
        await self.repository.create(developer)

    async def delete(self, developer_id: int) -> None:
        return await self.repository.delete(developer_id=developer_id)

    async def get(self, developer_id: int) -> Developer:
        return await self.repository.get(developer_id=developer_id)

    async def list(self, team: Optional[int], limit: int, offset: int) -> List[Developer]:
        return await self.repository.list(team=team, limit=limit, offset=offset)

    async def update(self, developer_id: int, developer: DeveloperCreateDTO) -> None:
        await self.repository.update(
            developer_id=developer_id,
            developer=developer,
        )
