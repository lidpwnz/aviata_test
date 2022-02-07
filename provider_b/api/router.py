import os

from fastapi import APIRouter


from services.parser import Parser

router = APIRouter(prefix='/api')


@router.post("/search")
async def search():
    return await Parser().parse_a(os.environ.get(
        'SERVICE_URL',
        '1eGlS-_4gAqY1LkJU0rXgzGxZrq9yfMXZ'
    ))
