from tortoise import Tortoise

Tortoise.init_models(["database.models.base"], "api")
Tortoise.init_models(["database.models.dynamic_models"], "plugins")

TORTOISE_ORM = {
    "connections": {
        "api": "postgres://postgres:1@127.0.0.1:5432/tmp",
        "plugins": "postgres://postgres:1@127.0.0.1:5432/dmc"
    },
    "apps": {
        "api": {
            "models": ["database.models.base", "aerich.models"],
            "default_connection": "api",
        },
        "plugins": {
            "models": ["database.models.dynamic_models", "aerich.models"],
            "default_connection": "plugins",
        },
    },
}


async def init():
    await Tortoise.init(TORTOISE_ORM)
    await Tortoise.generate_schemas()
