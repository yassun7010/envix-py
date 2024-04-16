from typing import assert_never

from envix.config.config import Config
from envix.config.v1.config import ConfigV1
from envix.exception import (
    EnvixEnvInjectionError,
)
from envix.loader.v1_loader import load_envs_v1
from envix.types import Secrets


async def load_envs(
    config: Config,
) -> tuple[Secrets, list[EnvixEnvInjectionError]]:
    total_secrets: Secrets = {}
    total_errors: list[EnvixEnvInjectionError] = []

    config_root = config.root
    match config_root:
        case ConfigV1():
            for envs in config_root.envs:
                secrets, errors = await load_envs_v1(envs)
                total_secrets.update(secrets)
                total_errors.extend(errors)

        case _:
            assert_never(config_root)

    return total_secrets, total_errors
