from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.settings import get_settings
from app.api.views.rooms import router as rooms_router
from app.api.views.auth import router as auth_router
from app.api.views.booking import router as booking_router
from app.api.views.rooms_type import router as rooms_type_router
from app.api.views.support_chat import router as support_chat_router

settings = get_settings()


def create_app() -> CORSMiddleware:
    app_ = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
    )
    app_.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    app_.include_router(rooms_router, prefix="/rooms", tags=["Rooms"])
    app_.include_router(booking_router, prefix="/booking", tags=["Booking"])
    app_.include_router(rooms_type_router, prefix="/room_types", tags=["Room Types"])
    app_.include_router(support_chat_router, prefix="/support_chat", tags=["Support Chat"])
    return CORSMiddleware(
        app_,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
