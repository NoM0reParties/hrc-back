from typing import List
from fastapi import Depends

from models import FeatureTeamOrder
from repositories import FeatureTeamOrderRepository
from repositories.developer_assignment import DeveloperAssignmentRepository
from schemas import FeatureTeamOrderBaseDTO
from schemas.developer_assignment import DeveloperAssignmentCreateDTO
from schemas.feature_team_order import FeatureTeamOrderUpdateDTO


class FeatureTeamOrderService:
    repository: FeatureTeamOrderRepository
    assignment_repository: DeveloperAssignmentRepository

    def __init__(
            self,
            repository: FeatureTeamOrderRepository = Depends(),
            assignment_repository: DeveloperAssignmentRepository = Depends(),
    ) -> None:
        self.repository = repository
        self.assignment_repository = assignment_repository

    async def create(self, order: FeatureTeamOrderBaseDTO) -> None:
        await self.repository.create(order=order)

    async def delete(self, order_id: int) -> None:
        return await self.repository.delete(order_id=order_id)

    async def get(self, order_id: int) -> FeatureTeamOrder:
        return await self.repository.get(order_id=order_id)

    async def list(self, limit: int, offset: int) -> List[FeatureTeamOrder]:
        return await self.repository.list(limit=limit, offset=offset)

    async def update(self, order_id: int, order: FeatureTeamOrderUpdateDTO) -> None:
        if order.developer_id is not None:
            order.auto_assignment = False
            order.assigned = True
            assignment = DeveloperAssignmentCreateDTO(developer_id=order.developer_id, feature_team_order_id=order_id)
            existing_assignment = await self.assignment_repository.find_existing_assignment(assignment=assignment)
            print('============>>>>>>>>>>>>>>>>', existing_assignment)
            if existing_assignment:
                await self.assignment_repository.delete(dev_assignment_id=existing_assignment.id)
            await self._create_assignment(assignment=assignment)
        await self.repository.update(order_id=order_id, order=order)

    async def _create_assignment(self, assignment: DeveloperAssignmentCreateDTO):
        await self.assignment_repository.create(assignment)

    async def _delete_assignment(self, dev_assignment_id: int):
        await self.assignment_repository.delete(dev_assignment_id=dev_assignment_id)
