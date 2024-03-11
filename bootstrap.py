"""
"""
from __future__ import annotations

import typing
from databases import Database
from datetime import timedelta, datetime
from arq import create_pool
from arq.connections import RedisSettings, ArqRedis
# from krispcall.common.core.settings import Settings
from webapi.webapi.config import AppSettings


from krispbroadcaster import KrispBroadcast
from database import DbConnection


class JobQueue:
    def __init__(
        self,
        redis_settings,
        skip_rpc: bool = False,
        default_queue_name: str = "arq:general_queue",
        rpc_queue_name: str = "arq:rpc_queue",
        sales_queue_name: str = "arq:sales_queue",
    ):
        self._redis: ArqRedis
        self._settings = redis_settings
        self._skip_rpc = skip_rpc
        self._default_queue_name = default_queue_name
        self._rpc_queue_name = rpc_queue_name
        self._sales_queue_name = sales_queue_name

    async def connect(self):
        self._redis = await create_pool(
            RedisSettings.from_dsn(self._settings),
            default_queue_name=self._default_queue_name,
        )

    async def enqueue_job(
        self,
        func: str,
        data: typing.Tuple[typing.Any, ...],
        *,
        job_id: typing.Optional[str] = None,
        defer_by_seconds: typing.Optional[float] = None,
        expires_in_seconds: typing.Optional[float] = None,
        defer_until: typing.Optional[datetime] = None,
        queue_name: typing.Optional[str] = None,
    ):
        return await self._redis.enqueue_job(  # type: ignore
            func,
            *data,
            _job_id=job_id,
            _queue_name=queue_name,
            _defer_by=None
            if defer_by_seconds is None
            else timedelta(seconds=defer_by_seconds),
            _expires=None
            if expires_in_seconds is None
            else timedelta(seconds=expires_in_seconds),
            _defer_until=defer_until,
        )

    async def run_task(
        self,
        func: str,
        *args: typing.Any,
        _job_id: typing.Optional[str] = None,
        _queue_name: typing.Optional[str] = None,
    ):
        """enqueue job in default queue"""
        await self._redis.enqueue_job(
            func, *args, _job_id=_job_id, _queue_name=_queue_name
        )

    async def call(
        self,
        func: str,
        *args: typing.Any,
        _job_id: typing.Optional[str] = None,
    ):
        # if self._skip_rpc:
        #     return None
        # """enqueue job and wait for result"""
        # job = await self._redis.enqueue_job(
        #     func, *args, _job_id=_job_id, _queue_name=self._rpc_queue_name
        # )
        # return await job.result()  # type: ignore
        """enqueue job and do not wait for result"""
        await self._redis.enqueue_job(
            func, *args, _job_id=_job_id, _queue_name=self._rpc_queue_name
        )

    async def sales_call(
        self,
        func: str,
        *args: typing.Any,
        defer_by_seconds: typing.Optional[float] = None,
        defer_until: typing.Optional[datetime] = None,
        _job_id: typing.Optional[str] = None,
    ):
        # if self._skip_rpc:
        #     return None
        # """enqueue job and wait for result"""
        # job = await self._redis.enqueue_job(
        #     func, *args, _job_id=_job_id, _queue_name=self._rpc_queue_name
        # )
        # return await job.result()  # type: ignore
        """enqueue job and do not wait for result"""
        await self._redis.enqueue_job(
            func,
            *args,
            _job_id=_job_id,
            _queue_name=self._sales_queue_name,
            _defer_by=None
            if defer_by_seconds is None
            else timedelta(seconds=defer_by_seconds),
            _defer_until=defer_until,
        )


def init_queue(settings: AppSettings) -> JobQueue:
    """initialize Job Queue"""
    return JobQueue(settings.redis_settings, skip_rpc=settings.is_testing)


def init_broadcaster(settings: AppSettings) -> KrispBroadcast:
    """initialize kafka client"""
    return KrispBroadcast(settings.broadcaster_dsn)


def init_worker_database(settings: AppSettings) -> Database:
    """load/unload postgres engine"""
    if settings.is_testing:
        return Database(
            settings.pg_dsn, ssl=settings.pg_use_ssl, force_rollback=True
        )
    return Database(
        settings.pg_dsn,
        ssl="require",
        min_size=settings.worker_pg_min_size,
        max_size=settings.worker_pg_max_size,
    )

def init_database(settings: AppSettings) -> Database:
    """load/unload postgres engine"""
    if settings.is_testing:
        return Database(
            settings.pg_dsn, ssl=settings.pg_use_ssl, force_rollback=True
        )
    return Database(
        settings.pg_dsn,
        ssl="disable",
        min_size=settings.pg_min_size,
        max_size=settings.pg_max_size,
    )