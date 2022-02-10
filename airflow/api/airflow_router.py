from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.config import get_db
from services.parser import Parser

router = APIRouter(
    prefix='/api',
)


@router.post('/search')
async def search(db: Session = Depends(get_db)):
    return await Parser().parse_providers(db)


@router.get('/results/{search_id}/{currency}/')
async def results(search_id: str, currency: str, db: Session = Depends(get_db)):
    return await Parser().search_by_id(search_id, db, currency)
