from pydantic import BaseModel, ConfigDict

from envix.config.v1.envix_v1 import EnvixV1

from .envs import EnvsV1


class ConfigV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    envix: EnvixV1
    envs: list[EnvsV1]
