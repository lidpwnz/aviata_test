from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.config import get_db
from db.repos.airflow_repo import AirflowRepo
from services.parser import Parser

router = APIRouter(
    prefix='/api',
)


@router.post('/search')
async def search(db: Session = Depends(get_db)):
    return await Parser().parse_providers(db)


@router.get('/results/{search_id}/')
async def results(search_id: str, db: Session = Depends(get_db)):
    return AirflowRepo(db).get(search_id=search_id, is_json=True)
