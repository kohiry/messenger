from fastapi import FastAPI

from app.user.router import user_router

app = FastAPI()
app.include_router(user_router)


@app.get('/')
def core() -> dict[str, str]:
    return {'hello': 'world'}