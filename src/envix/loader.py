import asyncio
import os

from typing import assert_never

from envix.config.config import Config
from envix.config.v1.config import ConfigV1
from envix.config.v1.envs import EnvsV1
from envix.config.v1.envs.google_cloud_secret_manager_envs_v1 import (
    GoogleCloudSecretManagerEnvsV1,
)
from envix.config.v1.envs.local_envs_v1 import LocalEnvsV1
from envix.config.v1.envs.raw_envs_v1 import RawEnvsV1
from envix.exception import (
    EnvixEnvInjectionError,
    EnvixEnvironmentNotSetting,
    EnvixGoogleCloudSecretManagerError,
)


async def load_raw_envs(
    envs: RawEnvsV1,
) -> tuple[list[str], list[EnvixEnvInjectionError]]:
    envnames: list[str] = []
    errors: list[EnvixEnvInjectionError] = []
    for envname, envvar in envs.items.items():
        if envs.overwrite or envname not in os.environ:
            os.environ[envname] = envvar
            envnames.append(envname)

    return envnames, errors


async def load_local_envs(
    envs: LocalEnvsV1,
) -> tuple[list[str], list[EnvixEnvInjectionError]]:
    envnames: list[str] = []
    errors: list[EnvixEnvInjectionError] = []
    for envname, envvar in envs._items.items():
        if envvar not in os.environ:
            errors.append(EnvixEnvironmentNotSetting(envvar))
            continue

        if envs.overwrite or envname not in os.environ:
            os.environ[envname] = os.environ[envvar]
            envnames.append(envname)

    return envnames, errors


async def load_google_cloud_secret_manager_envs(
    envs: GoogleCloudSecretManagerEnvsV1,
) -> tuple[list[str], list[EnvixEnvInjectionError]]:
    from google.cloud import secretmanager

    envnames: list[str] = []
    errors: list[EnvixEnvInjectionError] = []
    client = secretmanager.SecretManagerServiceAsyncClient()

    async def access_secret_version(envname: str, secret_name: str):
        if envs.overwrite or envname not in os.environ:
            try:
                response = await client.access_secret_version(
                    request={"name": secret_name}
                )
                envvar = response.payload.data.decode("UTF-8")
                os.environ[envname] = envvar
                envnames.append(envname)

            except Exception as e:
                errors.append(EnvixGoogleCloudSecretManagerError(envname, e))

    await asyncio.gather(
        *(
            access_secret_version(envname, secret_name)
            for envname, secret_name in envs.secret_items.items()
        )
    )

    return envnames, errors


async def load_envs_v1(
    envs: EnvsV1,
) -> tuple[list[str], list[EnvixEnvInjectionError]]:
    match envs:
        case RawEnvsV1():
            return await load_raw_envs(envs)

        case LocalEnvsV1():
            return await load_local_envs(envs)

        case GoogleCloudSecretManagerEnvsV1():
            return await load_google_cloud_secret_manager_envs(envs)

        case _:
            assert_never(envs)


async def load_envs(
    config: Config,
) -> tuple[list[str], list[EnvixEnvInjectionError]]:
    envnames: list[str] = []
    errors: list[EnvixEnvInjectionError] = []

    match config.root:
        case ConfigV1() as config_:
            for envs in config_.envs:
                envnames_, errors_ = await load_envs_v1(envs)
                envnames.extend(envnames_)
                errors.extend(errors_)

        case _:
            assert_never(config.root)

    return envnames, errors
