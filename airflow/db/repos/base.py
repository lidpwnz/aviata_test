import copy
import json
import logging
from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.engine import Result
from sqlalchemy.exc import DatabaseError, SQLAlchemyError
from sqlalchemy.orm import Session

from db.exceptions import NotFoundException
from db.models import Base


from sqlalchemy.ext.declarative import DeclarativeMeta


class BaseRepository:
    _model: Base = None

    def __init__(self, session: Session) -> None:
        self._db = session

    def not_found_error(self, **search_args: Any) -> None:
        args_to_string = ', '.join(f'{k}: {v}' for k, v in search_args)
        raise NotFoundException(f'{self._model.__name__} with params: {args_to_string} not found!')

    @staticmethod
    def not_found_exception_handler(callback, *args, **kwargs):
        try:
            return callback(*args, **kwargs)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))

    def get(self, pk: int = None, **search_args) -> dict:
        query = select(self._model)
        for k, v in search_args.items():
            query = query.where(getattr(self._model, k) == v)

        if pk and 'pk' not in search_args:
            query = query.where(self._model.id == pk)

        obj: Result = self._db.execute(query)
        result = obj.scalars().all()

        if not result:
            self.not_found_error(**search_args)

        return result

    def add(self, scheme: BaseModel) -> Base:
        try:
            obj = self._model(**scheme.dict())  # Создать инстанс модели
            self._db.add(obj)   # Добавить инстанс в сессию (фактически insert-запрос)
            self._db.flush()    # Примерить изменения на базе
            result = copy.deepcopy(obj)     # Копируем инстанс в новую переменную
            self._commit()   # Выполняем запрос
            return result
        except DatabaseError:   # Отлавливаем ошибку и делаем роллбэк
            self._db.rollback()
            raise

    def all(self) -> dict:
        return self._db.execute(select(self._model).where(self._model.is_deleted == False)).scalars().all()

    def update(self, scheme: BaseModel, pk: int) -> dict:
        is_exists = self._db.execute(select(self._model).where(self._model.id == pk))
        if not is_exists:
            self.not_found_error(pk=pk)

        request = update(self._model).where(self._model.id == pk)

        for k, v in scheme.dict().items():
            if v:
                request = request.values(**{k: v})

        self._commit(request)
        return self.get(pk=pk)

    def delete(self, pk: int, field_name: str = 'is_deleted', permanent: bool = False):
        query = None

        if hasattr(self._model, field_name) and not permanent:
            query = self._db.execute(update(self._model).where(self._model.id == pk).values(is_deleted=True))
        if permanent:
            query = self._db.execute(delete(self._model).where(self._model.id == pk))
        if query.rowcount == 0:
            self.not_found_error(pk=pk)

        self._commit()

    def _commit(self, query=None) -> None:
        try:
            if query is not None:
                self._db.execute(query)
            else:
                self._db.flush()    # Примерить изменения на базе
            self._db.commit()
        except SQLAlchemyError:
            self._db.rollback()
            raise
        finally:
            self._db.close()
