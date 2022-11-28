from typing import List, Optional

from fastapi import APIRouter, Depends, status

from schemas import FeatureDTO, FeatureBaseDTO, FeatureResponseDTO
from services import FeatureService

FeatureRouter = APIRouter(
    prefix="/features", tags=["feature"]
)


@FeatureRouter.get("/sprint/{sprint_id}", response_model=List[FeatureDTO])
async def index(
        sprint_id: int,
        service: FeatureService = Depends(),
):
    return await service.list_by_sprint(sprint_id)


@FeatureRouter.get("/", response_model=List[FeatureResponseDTO])
async def index(
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
        service: FeatureService = Depends(),
):
    return [feature.normalize() for feature in (await service.list(limit=limit, offset=offset))]


@FeatureRouter.get("/{feature_id}", response_model=FeatureResponseDTO)
async def get(feature_id: int, service: FeatureService = Depends()):
    return (await service.get(feature_id=feature_id)).normalize()


@FeatureRouter.post(
    "/",
    response_model=FeatureResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create(
        feature: FeatureBaseDTO,
        service: FeatureService = Depends(),
):
    return await service.create(feature)


@FeatureRouter.put("/{feature_id}")
async def update(
        feature_id: int,
        feature: FeatureBaseDTO,
        service: FeatureService = Depends(),
):
    return await service.update(feature_id, feature)


@FeatureRouter.delete(
    "/{feature_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
        feature_id: int, service: FeatureService = Depends()
):
    return await service.delete(feature_id)
