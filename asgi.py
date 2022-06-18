from fastapi import FastAPI

app = FastAPI(
    title="TemplateProject",
)


@app.get("/")
async def root():
    return {"message": "Root endpoint works!"}
