from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.api.v1 import v1_router
from src.config import settings
from src.core.exceptions import (
    BusinessLogicError,
    ExternalAPIError,
    NotFoundError,
)
from src.system.logging import setup_logging
from src.system.resources import IoCContainer


def create_app() -> FastAPI:
    container = IoCContainer()

    setup_logging(
        log_level=settings.LOG_LEVEL,
        log_file=settings.LOG_FILE,
        log_in_console=settings.LOG_IN_CONSOLE,
    )

    application = FastAPI(title="Travel Planner API", version="1.0.0")
    application.container = container

    application.include_router(v1_router)

    @application.exception_handler(NotFoundError)
    async def not_found_handler(request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"detail": exc.detail})

    @application.exception_handler(BusinessLogicError)
    async def business_logic_handler(request, exc: BusinessLogicError):
        return JSONResponse(status_code=400, content={"detail": exc.detail})

    @application.exception_handler(ExternalAPIError)
    async def external_api_handler(request, exc: ExternalAPIError):
        return JSONResponse(status_code=502, content={"detail": exc.detail})

    return application


app = create_app()
