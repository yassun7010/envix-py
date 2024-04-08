from argparse import ArgumentParser, _SubParsersAction
from pathlib import Path
from typing import Any, cast

from pydantic import BaseModel


class Args(BaseModel):
    command: str
    args: list[str]
    config_file: Path


def add_subparser(subparsers: "_SubParsersAction[Any]", **kwargs: Any) -> None:
    help = "Inject environment variables and execute the command."

    parser = cast(
        ArgumentParser,
        subparsers.add_parser(
            "inject",
            description=help,
            help=help,
            **kwargs,
        ),
    )

    parser.add_argument(
        "command",
        metavar="COMMAND",
    )

    parser.add_argument("args", metavar="ARGS", nargs="*")

    parser.add_argument(
        "--config-file",
        metavar="CONFIG_FILE",
        help="config file path.",
        type=Path,
        default="envix.toml",
    )

    parser.set_defaults(handler=lambda space: inject_command(Args(**vars(space))))


def inject_command(args: Args) -> None:
    import asyncio
    import subprocess

    from envix.config.config import Config
    from envix.exception import EnvixInjectionError
    from envix.loader import load_envs

    config = Config.load(args.config_file)

    _, errors = asyncio.run(load_envs(config))

    if errors:
        raise EnvixInjectionError(errors)

    subprocess.call([args.command] + args.args)
