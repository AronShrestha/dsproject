"""
database driver connection protocol

maybe dbapi provides database connection protocol class
"""
# pylint: disable=missing-class-docstring, missing-function-docstring
from __future__ import annotations

import typing
from pydantic import BaseModel
from uuid import UUID


ClauseElement = typing.TypeVar("ClauseElement")

class Repository(typing.Protocol):
    """
    base repository protocol,
    should not be instantiated

    subclasses should also be protocols
    """

    def add(self, model: BaseModel) -> None:
        raise NotImplementedError()

    def get(self, ref: UUID) -> BaseModel:
        raise NotImplementedError()



class DbTransaction(typing.Protocol):
    async def start(self) -> None:
        raise NotImplementedError()  # pragma: no cover

    async def commit(self) -> None:
        raise NotImplementedError()  # pragma: no cover

    async def rollback(self) -> None:
        raise NotImplementedError()  # pragma: no cover


class DbConnection(typing.Protocol):
    async def commit(self) -> None:
        raise NotImplementedError()

    async def rollback(self) -> None:
        raise NotImplementedError()

    async def transaction(self) -> DbTransaction:
        raise NotImplementedError()

    async def execute(self, query: ClauseElement) -> typing.Any:
        raise NotImplementedError()

    async def execute_many(self, query: typing.List[ClauseElement]) -> None:
        raise NotImplementedError()

    async def fetch_all(
        self, query: ClauseElement
    ) -> typing.List[typing.Mapping[str, typing.Any]]:
        raise NotImplementedError()

    async def fetch_one(
        self, query: ClauseElement
    ) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        raise NotImplementedError()

    async def fetch_val(self, query: ClauseElement) -> typing.Any:
        raise NotImplementedError()


class SqlAlchemyRepository(Repository, typing.Protocol):
    db: DbConnection

    def __init__(self, db: DbConnection):
        ...
