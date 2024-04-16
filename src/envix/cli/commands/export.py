import asyncio
import json
from argparse import ArgumentParser, FileType, _SubParsersAction
from io import TextIOWrapper
from pathlib import Path
from shlex import quote
from typing import Annotated, Any, Literal, assert_never, cast, get_args

from pydantic import BaseModel, ConfigDict

from envix.cli.default import AUTO_SEARCH, STDOUT
from envix.cli.field import ConfigFileValidator, OutputFileValidator
from envix.config.config import Config
from envix.exception import EnvixLoadEnvsError
from envix.loader import load_envs

OutputFormat = Literal["dotenv", "json"]


class Args(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    config_file: Annotated[Path | None, ConfigFileValidator]
    output_file: Annotated[TextIOWrapper | None, OutputFileValidator]
    format: OutputFormat


def add_subparser(subparsers: "_SubParsersAction[Any]", **kwargs: Any) -> None:
    help = "Output environment variables to a file."

    parser = cast(
        ArgumentParser,
        subparsers.add_parser(
            "export",
            description=help,
            help=help,
            **kwargs,
        ),
    )

    parser.add_argument(
        "--config-file",
        metavar="CONFIG_FILE",
        help="config file path.",
        type=Path,
        default=AUTO_SEARCH,
    )

    parser.add_argument(
        "--output-file",
        "-o",
        help="output file path.",
        type=FileType("w"),
        default=STDOUT,
    )

    parser.add_argument(
        "--format",
        help="output format.",
        choices=get_args(OutputFormat),
        default="dotenv",
    )

    parser.set_defaults(handler=lambda space: export_command(Args(**vars(space))))


def export_command(args: Args) -> None:
    config = Config.load(args.config_file)
    secrets, errors = asyncio.run(load_envs(config))
    if errors:
        raise EnvixLoadEnvsError(errors)

    match args.format:
        case "dotenv":
            print(
                "\n".join(
                    f"{envname}={quote(secret.get_secret_value())}"
                    for envname, secret in secrets.items()
                ),
                file=args.output_file,
            )

        case "json":
            print(
                json.dumps(
                    {
                        envname: secret.get_secret_value()
                        for envname, secret in secrets.items()
                    }
                ),
                file=args.output_file,
            )

        case _:
            assert_never(args.format)
