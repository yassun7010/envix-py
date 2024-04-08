from pathlib import Path
from typing import Self

from pydantic import RootModel

from envix.exception import EnvixConfigFileExtensionError, EnvixConfigFileNotFound

from .v1.config import ConfigV1


class Config(RootModel):
    root: ConfigV1

    @classmethod
    def load(cls, filepath: Path) -> Self:
        import tomllib

        if not filepath.exists():
            raise EnvixConfigFileNotFound(filepath)

        match filepath.suffix:
            case ".toml":
                with open(filepath, "rb") as f:
                    return cls.model_validate(tomllib.load(f))

            case ".yaml" | ".yml":
                import yaml

                with open(filepath, "rb") as f:
                    return cls.model_validate(yaml.safe_load(f))

            case _:
                raise EnvixConfigFileExtensionError(filepath)
