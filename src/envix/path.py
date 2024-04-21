import os
from pathlib import Path


def get_config(name: str) -> Path:
    return get_user_config_dir().joinpath("config", "envix_{name}.yml")


def list_config() -> list[Path]:
    return list(get_user_config_dir().joinpath("config").glob("envix_*.yml"))


def get_user_config_dir() -> Path:
    config_dir: Path
    if path := os.getenv("ENVIX_CONFIG_DIR"):
        config_dir = Path(path)

    elif path := os.getenv("XDG_CONFIG_HOME"):
        config_dir = Path(path).joinpath("envix")

    else:
        config_dir = Path.home().joinpath(".config/envix")

    if not config_dir.joinpath("config").exists():
        config_dir.mkdir(parents=True, exist_ok=True)

    return config_dir
