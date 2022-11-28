from typing import List, Optional

from fastapi import APIRouter, Depends, status

from schemas import DevTeamBaseDTO, DevTeamDTO
from services import DeveloperTeamService

DevTeamRouter = APIRouter(
    prefix="/developer-teams", tags=["dev_team"]
)


@DevTeamRouter.get("/", response_model=List[DevTeamDTO])
async def index(
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
        service: DeveloperTeamService = Depends(),
):
    return [
        dt.normalize()
        for dt in await service.list(
            limit=limit,
            offset=offset,
        )
    ]


@DevTeamRouter.get("/{dev_team_id}", response_model=DevTeamDTO)
async def get(dev_team_id: int, service: DeveloperTeamService = Depends()):
    return (await service.get(dev_team_id=dev_team_id)).normalize()


@DevTeamRouter.post(
    "/",
    response_model=DevTeamDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create(
        dev_team: DevTeamBaseDTO,
        service: DeveloperTeamService = Depends(),
):
    return await service.create(dev_team=dev_team)


@DevTeamRouter.patch("/{dev_team_id}", response_model=DevTeamDTO)
async def update(
        dev_team_id: int,
        dev_team: DevTeamBaseDTO,
        service: DeveloperTeamService = Depends(),
):
    return (await service.update(dev_team_id=dev_team_id, dev_team=dev_team)).normalize()


@DevTeamRouter.delete(
    "/{dev_team_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
        dev_team_id: int, service: DeveloperTeamService = Depends()
):
    return await service.delete(dev_team_id=dev_team_id)
