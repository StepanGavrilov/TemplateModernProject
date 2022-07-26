import sentry_sdk

from config import config
sentry_service = sentry_sdk.init(
    dsn=config.get("SENTRY_DSN"),
    traces_sample_rate=1.0
)
