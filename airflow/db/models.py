from uuid import uuid4

import sqlalchemy
import sqlalchemy_jsonfield
import ujson
from sqlalchemy.orm import declared_attr, declarative_base


class CustomBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=CustomBase)


class AirflowResults(Base):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    search_id = sqlalchemy.Column(sqlalchemy.String(36), default=str(uuid4()))
    status = sqlalchemy.Column(sqlalchemy.String(10), default='PENDING')
    items = sqlalchemy.Column(sqlalchemy_jsonfield.JSONField(
        enforce_string=False,
        enforce_unicode=False,
        json=ujson
    ))
