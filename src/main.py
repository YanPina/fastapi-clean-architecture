from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.interfaces.api.router import router

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

# set CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin) for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/", tags=["System"])  # type: ignore[misc]
def root() -> str:
    return "service is working"


app.include_router(router, prefix=settings.API_V1_STR)
