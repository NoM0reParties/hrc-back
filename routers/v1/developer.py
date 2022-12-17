from typing import List, Optional

from fastapi import APIRouter, Depends, status

from schemas import DeveloperCreateDTO, DeveloperDTO
from services import DeveloperService

DeveloperRouter = APIRouter(
    prefix="/developers", tags=["developer"]
)


@DeveloperRouter.get("/", response_model=List[DeveloperDTO])
async def index(
        team: Optional[int] = None,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
        service: DeveloperService = Depends(),
):
    return [
        d.normalize()
        for d in await service.list(
            team=team,
            limit=limit,
            offset=offset,
        )
    ]


@DeveloperRouter.get("/{developer_id}", response_model=DeveloperDTO)
async def get(developer_id: int, service: DeveloperService = Depends()):
    return (await service.get(developer_id=developer_id)).normalize()


@DeveloperRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create(
        developer: DeveloperCreateDTO,
        service: DeveloperService = Depends(),
):
    await service.create(developer)


@DeveloperRouter.put("/{developer_id}")
async def update(
        developer_id: int,
        developer: DeveloperCreateDTO,
        service: DeveloperService = Depends(),
):
    await service.update(developer_id, developer)


@DeveloperRouter.delete(
    "/{developer_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
        developer_id: int, service: DeveloperService = Depends()
):
    return await service.delete(developer_id)
