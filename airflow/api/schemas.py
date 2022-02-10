from typing import List

from pydantic import BaseModel


class AirflowScheme(BaseModel):
    search_id: str
    status: str
    items: List[dict]
