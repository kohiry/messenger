from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def core() -> dict[str, str]:
    return {'hello': 'world'}