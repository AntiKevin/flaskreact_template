from fastapi.routing import APIRouter

from template.web.api import monitoring, user, auth

api_router = APIRouter()
api_router.include_router(monitoring.router)

api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
