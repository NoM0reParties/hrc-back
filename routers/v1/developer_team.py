from typing import List, Optional

from fastapi import APIRouter, Depends, status

from schemas import DevTeamBaseDTO, DevTeamDTO
from schemas.developer_team import DevTeamBySprintDTO, DevTeamWithDevelopersDTO
from services import DeveloperTeamService

DevTeamRouter = APIRouter(
    prefix="/developer-teams", tags=["dev_team"]
)


@DevTeamRouter.get("/", response_model=List[DevTeamWithDevelopersDTO])
async def index(
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
        service: DeveloperTeamService = Depends(),
):
    return await service.list(limit=limit, offset=offset)


@DevTeamRouter.get("/sprint/{sprint_id}", response_model=List[DevTeamBySprintDTO])
async def index(
        sprint_id: int,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
        service: DeveloperTeamService = Depends(),
):
    return await service.list_by_sprint(sprint_id=sprint_id, limit=limit, offset=offset)


@DevTeamRouter.get("/{dev_team_id}", response_model=DevTeamDTO)
async def get(dev_team_id: int, service: DeveloperTeamService = Depends()):
    return (await service.get(dev_team_id=dev_team_id)).normalize()


@DevTeamRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create(
        dev_team: DevTeamBaseDTO,
        service: DeveloperTeamService = Depends(),
):
    return await service.create(dev_team=dev_team)


@DevTeamRouter.put("/{dev_team_id}")
async def update(
        dev_team_id: int,
        dev_team: DevTeamBaseDTO,
        service: DeveloperTeamService = Depends(),
):
    return await service.update(dev_team_id=dev_team_id, dev_team=dev_team)


@DevTeamRouter.delete(
    "/{dev_team_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
        dev_team_id: int, service: DeveloperTeamService = Depends()
):
    return await service.delete(dev_team_id=dev_team_id)
