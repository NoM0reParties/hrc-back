from typing import List, Optional

from fastapi import APIRouter, Depends, status

from schemas import SprintDTO, SprintBaseDTO
from services import SprintService

SprintRouter = APIRouter(
    prefix="/sprints", tags=["sprint"]
)


@SprintRouter.get("/", response_model=List[SprintDTO])
async def index(
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
        service: SprintService = Depends(),
):
    return [
        sprint.normalize()
        for sprint in await service.list(
            limit=limit,
            offset=offset,
        )
    ]


@SprintRouter.get("/{sprint_id}", response_model=SprintDTO)
async def get(sprint_id: int, service: SprintService = Depends()):
    return (await service.get(sprint_id=sprint_id)).normalize()


@SprintRouter.post(
    "/",
    response_model=SprintDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create(
        sprint: SprintBaseDTO,
        service: SprintService = Depends(),
):
    return await service.create(sprint)


@SprintRouter.patch("/{sprint_id}")
async def update(
        sprint_id: int,
        sprint: SprintBaseDTO,
        service: SprintService = Depends(),
):
    return await service.update(sprint_id, sprint)


@SprintRouter.delete(
    "/{sprint_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
        sprint_id: int, service: SprintService = Depends()
):
    return await service.delete(sprint_id)
