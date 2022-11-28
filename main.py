from fastapi import FastAPI

from configs.environment import get_environment_variables
from metadata.tags import tags
from routers import v1_router

# Application Environment Configuration
env = get_environment_variables()

# Core Application Instance
app = FastAPI(
    debug=True,
    title=env.APP_NAME,
    version=env.API_VERSION,
    openapi_tags=tags,
)

# Add Routers
app.include_router(v1_router)
