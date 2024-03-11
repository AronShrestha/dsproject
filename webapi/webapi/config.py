"""
application settings
"""
from __future__ import annotations

import typing
from pathlib import Path
from uuid import UUID
from functools import lru_cache
from yaml import safe_load
import logging
import os
import sys
LOGGER = logging.getLogger(__name__)

from pydantic import PositiveInt, BaseSettings, ValidationError
from pydantic.types import SecretStr



ENV_PREFIX = "KRISPCALL_"
APP_PATH = Path(__file__).parent
BASE_PATH = APP_PATH.parent
API_BASE_VERSION = "v1"


class AppSettings(BaseSettings):
    is_testing= False
    worker_pg_min_size: int = 2
    worker_pg_max_size: int = 3
    pg_min_size: int = 2
    pg_max_size: int = 3
    base_path: Path
    app_id: str = "com.ds.webapi"
    app_name: str = "webapi"
    app_env: str = "development"
    allowed_media_types: typing.Tuple[str, ...] = (
        "image/png",
        "image/jpg",
        "image/jpeg",
    )
    broadcaster_dsn:str = ""
    bulksms_estimation_cost_multiplier:float = 1.1
    bulksms_refund_time:int = 10
    debug: bool = True
    domain_host:str = "local"
    app_uri: str = ""
    pg_dsn: str = ""
    pg_use_ssl: str = ""
    redis_settings: str = ""
    secret_key: SecretStr = ""

    components: typing.List[str] = [
        "foundation"
    ]
    allowed_media_types: typing.Tuple[str, ...] = (
        "image/png",
        "image/jpg",
        "image/jpeg",
    )

    jwt_auth_token_lifetime_minutes: PositiveInt = typing.cast(
        PositiveInt, 1 * 7 * 24 * 60
    )
    jwt_access_token_lifetime_minutes: PositiveInt = typing.cast(
        PositiveInt, 1 * 7 * 24 * 60  # 1 week
    )
    jwt_refresh_token_lifetime_minutes: PositiveInt = typing.cast(
        PositiveInt, 2 * 7 * 24 * 60  # 2 week
    )

    jwt_reset_token_lifetime_minutes: PositiveInt = typing.cast(
        PositiveInt, 20  # 20 min
    )
    cors_allow_origins: typing.List[str] = ["*"]

    cors_allow_methods: typing.Tuple[str, ...] = (
        "GET",
        "POST",
        "DELETE",
        "PUT",
        "PATCH",
        "HEAD",
        "OPTIONS",
    )
    cors_allow_credentials: bool = False
    cors_expose_headers: typing.List[str] = []
    cors_allow_headers: typing.List[str] = ["*"]
    cors_max_age: int = 600
    session_lifetime: int = 7 * 86400



    class Config:  # pylint: disable=too-few-public-methods
        env_prefix = ENV_PREFIX



def _load_config(
    app_env: str, config_dir: Path
) -> typing.Dict[typing.Any, typing.Any]:
    """load config file"""
    config_file = config_dir.joinpath(f"{app_env}.yaml")
    if not config_file.exists():
        raise ValueError(f"Config file {config_file} doesn't exists")
    LOGGER.info("Found configuration ... %s", config_file)
    print(safe_load(open(config_file, "r").read()))
    return safe_load(open(config_file, "r").read())

    
def settings_factory(
    settings_class: typing.Type[BaseSettings], env_prefix: str, base_path: Path
) -> BaseSettings:
    """generate settings object using provided class"""
    app_env = os.getenv(env_prefix + "APP_ENV", "production")
    config_dir = base_path.joinpath("config")
    try:
        settings = settings_class(
            _env_file=f"{app_env}.env",
            base_path=base_path,
            app_env=app_env,
            **_load_config(app_env, config_dir),
        )
    except ValidationError as e:
        LOGGER.error("Invalid Config/Settings.")
        print(e)
        sys.exit(-1)
    else:
        return settings



@lru_cache()
def get_application_settings(env_prefix=ENV_PREFIX, base_path=BASE_PATH):
    return settings_factory(
        settings_class=AppSettings,
        env_prefix=env_prefix,
        base_path=base_path,
    )

