import os
from argparse import ArgumentParser, _SubParsersAction
from pathlib import Path
from typing import Annotated, Any, cast

from pydantic import BaseModel

from envix.cli.field import ConfigFileValidator


class Args(BaseModel):
    command: str
    args: list[str]
    config_file: Annotated[Path | None, ConfigFileValidator]
    config_name: list[str] | None
    clear_environments: bool


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
        "--file",
        metavar="CONFIG_FILE",
        help="config file path.",
        type=Path,
        default=None,
    )

    parser.add_argument(
        "--config-name",
        "--config",
        metavar="CONFIG_NAME",
        help="user registered setting name.",
        type=str,
        nargs="*",
    )

    parser.add_argument(
        "--clear-environments",
        action="store_true",
        help="Running commands with no environment variables set.",
        default=False,
    )

    parser.set_defaults(handler=lambda space: inject_command(Args(**vars(space))))


def inject_command(args: Args) -> None:
    import asyncio
    import subprocess

    from envix.config.config import load_configs
    from envix.exception import EnvixEnvInjectionError, EnvixLoadEnvsError
    from envix.loader import load_envs

    total_errors: list[EnvixEnvInjectionError] = []

    if args.clear_environments:
        os.environ.clear()

    for config in load_configs(args.config_file, args.config_name):
        _, errors = asyncio.run(load_envs(config))

        total_errors.extend(errors)

    if total_errors:
        raise EnvixLoadEnvsError(total_errors)

    subprocess.call([args.command] + args.args)
