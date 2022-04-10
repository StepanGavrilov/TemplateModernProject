from fastapi import FastAPI

app = FastAPI(
    title="TemplateProject",
)


@app.get("/")
async def minio():
    return {"message": "Root endpoint works!"}
