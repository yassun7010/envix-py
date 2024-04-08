from abc import ABC, abstractmethod
from pathlib import Path


class EnvixError(Exception, ABC):
    @property
    @abstractmethod
    def message(self) -> str: ...

    def __str__(self) -> str:
        return self.message


class EnvixConfigFileExtensionError(EnvixError, ValueError):
    def __init__(self, filename: Path):
        self.filename = filename

    @property
    def message(self) -> str:
        return f"Unsupported file format: {self.filename.suffix}"


class EnvixInjectionError(EnvixError):
    def __init__(self, errors: list["EnvixEnvInjectionError"]) -> None:
        self.errors = errors

    @property
    def message(self) -> str:
        return "\n".join(map(str, self.errors))


class EnvixConfigFileNotFound(EnvixError, FileNotFoundError):
    def __init__(self, filename: Path):
        self.filename = filename

    @property
    def message(self) -> str:
        return f"Config file not found: {self.filename}"


class EnvixEnvInjectionError(EnvixError, ValueError):
    pass


class EnvixEnvironmentNotSetting(EnvixEnvInjectionError):
    def __init__(self, envname: str):
        self.envname = envname

    @property
    def message(self) -> str:
        return f"Environment variable not set: {self.envname}"


class EnvixGoogleCloudSecretManagerError(EnvixEnvInjectionError):
    def __init__(self, envname: str, error: Exception):
        self.envname = envname
        self.error = error

    @property
    def message(self) -> str:
        return f"Google Cloud Secret Manager error: {self.envname}, {self.error}"
