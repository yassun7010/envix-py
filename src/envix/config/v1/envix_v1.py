from typing import Literal

from pydantic import BaseModel, ConfigDict


class EnvixV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: Literal[1]
