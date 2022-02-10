import requests

from api.schemas import AirflowScheme
from db.repos.airflow_repo import AirflowRepo
from services.helpers import get_search_id


class Parser:
    async def get_items(self):
        provider_a = requests.post("http://provider_a:8000/api/search/")
        provider_b = requests.post("http://provider_b:8001/api/search/")

        return provider_a.json() + provider_b.json()

    async def parse_providers(self, session):
        repo = AirflowRepo(session)

        data = {
            "items": await self.get_items(),
            "status": "COMPLETED",
            "search_id": str(await get_search_id())
        }

        repo.add(AirflowScheme(**data))
        return {'search_id': data.get('search_id')}
