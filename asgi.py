from pathlib import Path
from fastapi import FastAPI, Request
from custum_logging import CustomizeLogger

config_path = Path("logging_config.json")


def create_app() -> FastAPI:
    """
    Create app and custom logger
    """
    fast_api = FastAPI(title='CustomLogger', debug=False)
    logger = CustomizeLogger.make_logger(config_path)
    fast_api.logger = logger  # type: ignore
    return fast_api


app = create_app()


@app.get("/")
async def root(request: Request):
    print(request.app.logger.info("Root EndPoint."))
    return {"message": "Root endpoint works!"}
