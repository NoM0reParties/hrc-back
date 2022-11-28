from typing import List, Optional

from fastapi import APIRouter, Depends, status

from schemas import FeatureTeamOrderBaseDTO, FeatureTeamOrderDTO, FeatureTeamOrderResponseDTO
from schemas.feature_team_order import FeatureTeamOrderUpdateDTO
from services import FeatureTeamOrderService

FeatureTeamOrderRouter = APIRouter(
    prefix="/feature-team-orders", tags=["feature_team_order"]
)


@FeatureTeamOrderRouter.get("/", response_model=List[FeatureTeamOrderResponseDTO])
async def index(
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
        service: FeatureTeamOrderService = Depends(),
):
    return [
        fto.normalize()
        for fto in await service.list(
            limit=limit,
            offset=offset,
        )
    ]


@FeatureTeamOrderRouter.get("/{order_id}", response_model=FeatureTeamOrderDTO)
async def get(order_id: int, service: FeatureTeamOrderService = Depends()):
    return (await service.get(order_id=order_id)).normalize()


@FeatureTeamOrderRouter.post(
    "/",
    response_model=FeatureTeamOrderDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create(
        order: FeatureTeamOrderBaseDTO,
        service: FeatureTeamOrderService = Depends(),
):
    return await service.create(order)


@FeatureTeamOrderRouter.put("/{order_id}")
async def update(
        order_id: int,
        order: FeatureTeamOrderUpdateDTO,
        service: FeatureTeamOrderService = Depends(),
):
    await service.update(order_id, order)


@FeatureTeamOrderRouter.delete(
    "/{order_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
        order_id: int, service: FeatureTeamOrderService = Depends()
):
    return await service.delete(order_id)
