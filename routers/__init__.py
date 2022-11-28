from fastapi import APIRouter
from routers.v1 import *

v1_router = APIRouter(
    prefix="/v1", tags=["v1"]
)

v1_router.include_router(SprintRouter)
v1_router.include_router(DevTeamRouter)
v1_router.include_router(DeveloperRouter)
v1_router.include_router(FeatureRouter)
v1_router.include_router(FeatureTeamOrderRouter)
