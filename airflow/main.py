from fastapi import FastAPI

from api.airflow_router import router
from services.helpers import get_currencies

app = FastAPI()

app.include_router(router)


@app.on_event('startup')
async def startup():
    await get_currencies()
