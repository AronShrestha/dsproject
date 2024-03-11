""" Loads settings"""

from __future__ import annotations
import typing
from pathlib import Path
from functools import lru_cache
import os
import logging
LOGGER = logging.getLogger(__name__)
from yaml import safe_load
import sys


from pydantic import (
    BaseSettings,
    SecretStr,
    ValidationError,
)


ENV_PREFIX = "SALESAPI_"
APP_PATH = Path(__file__).parent
BASE_PATH = APP_PATH.parent
API_BASE_VERSION = "v1"


class AppSettings(BaseSettings):
    app_id: str = "com.ds.salesapi"
    app_name: str = "salesapi"
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
    base_path: Path
    is_testing: bool = False
    pg_min_size: int = 2
    pg_max_size: int = 3
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

