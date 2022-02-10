import json
import logging
import uuid

import httpx
import xmltodict


async def get_search_id():
    return uuid.uuid4()


async def get_currencies():
    logging.warning('HELLOSADLASLDLASL')
    xml_response = httpx.get('https://www.nationalbank.kz/rss/get_rates.cfm?fdate=26.10.2021')
    currencies_json = xmltodict.parse(xml_response.content)

    with open('currencies.json', 'w') as f:
        data = currencies_json['rates']['item']
        json.dump(data, f, ensure_ascii=False, indent=4)
