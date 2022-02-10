from db.models import AirflowResults
from db.repos.base import BaseRepository


class AirflowRepo(BaseRepository):
    _model = AirflowResults
