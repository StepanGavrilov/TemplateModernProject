from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from logg.custom_logging import custom_logger  # type: ignore
from sentry import sentry_service  # noqa: F401


def create_app() -> FastAPI:
    """
    Create app and custom logger
    """
    fast_api = FastAPI(title='CustomLogger', debug=False)
    fast_api.logger = custom_logger  # type: ignore
    return fast_api


app = create_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@custom_logger.catch()
@app.get("/")
async def root(request: Request):
    return {"message": f"Root endpoint works, {request.base_url}"}
