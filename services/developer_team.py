from typing import List
from fastapi import Depends

from models import DeveloperTeam
from repositories import DeveloperTeamRepository
from schemas import DevTeamBaseDTO


class DeveloperTeamService:
    repository: DeveloperTeamRepository

    def __init__(
            self, repository: DeveloperTeamRepository = Depends()
    ) -> None:
        self.repository = repository

    async def create(self, dev_team: DevTeamBaseDTO) -> DeveloperTeam:
        return await self.repository.create(dev_team=dev_team)

    async def delete(self, dev_team_id: int) -> None:
        return await self.repository.delete(dev_team_id=dev_team_id)

    async def get(self, dev_team_id: int) -> DeveloperTeam:
        return await self.repository.get(dev_team_id=dev_team_id)

    async def list(self, limit: int, offset: int) -> List[DeveloperTeam]:
        return await self.repository.list(limit=limit, offset=offset)

    async def update(self, dev_team_id: int, dev_team: DevTeamBaseDTO) -> DeveloperTeam:
        return await self.repository.update(
            dev_team_id=dev_team_id,
            dev_team=dev_team,
        )
