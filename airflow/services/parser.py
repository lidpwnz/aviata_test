import json
from decimal import Decimal
from typing import List

import grequests
from sqlalchemy.orm import Session

from api.schemas import AirflowScheme
from db.repos.airflow_repo import AirflowRepo
from services.helpers import get_search_id


class Parser:
    def __init__(self, session: Session) -> None:
        self.currencies = {'KZT': 1}
        self.repo = AirflowRepo(session)
        self.get_currencies()

    def get_currencies(self) -> None:
        with open('../currencies.json', 'r') as f:
            currencies = json.load(f)

            for item in currencies:
                self.currencies[item['title']] = item['description']

    async def get_items(self) -> List[dict]:
        providers = [
            "http://provider_a:8000/api/search/",
            "http://provider_b:8001/api/search/"
        ]

        provider_a, provider_b = grequests.map([grequests.post(url) for url in providers])

        return provider_a.json() + provider_b.json()

    async def get_currency_diff(self, currency: str) -> str:
        return self.currencies[currency]

    async def conversion(self, amount: str, current_currency: str, transfer_currency: str) -> str:
        current_currency = Decimal(await self.get_currency_diff(current_currency))
        transfer_currency = Decimal(await self.get_currency_diff(transfer_currency))

        result = Decimal(amount) * current_currency / transfer_currency
        return str(result.quantize(Decimal('1.00')))

    async def calculate_price(self, item, currency: str) -> None:
        pricing_info = item['pricing']
        converted_amount = await self.conversion(pricing_info['total'], pricing_info['currency'], currency)

        price = {
            'amount': converted_amount,
            'currency': currency
        }

        item.update({'price': price})

    async def convert_items_price(self, items: list, currency: str) -> List[dict]:
        for item in items:
            await self.calculate_price(item, currency)

        return items

    async def parse_providers(self) -> dict:
        data = {
            "items": await self.get_items(),
            "status": "COMPLETED",
            "search_id": str(await get_search_id())
        }

        self.repo.add(AirflowScheme(**data))
        return {'search_id': data.get('search_id')}

    async def search_by_id(self, search_id: str, currency: str) -> AirflowScheme:
        query_res = self.repo.get(search_id=search_id)[0]
        query_res.items = await self.convert_items_price(query_res.items, currency)

        return AirflowScheme(**query_res.__dict__)
