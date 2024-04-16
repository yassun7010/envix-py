import asyncio
import json
import pipes
from argparse import ArgumentParser, FileType, _SubParsersAction
from io import TextIOWrapper
from pathlib import Path
from typing import Any, Literal, assert_never, cast, get_args

from pydantic import BaseModel, ConfigDict, field_validator

from envix._helper import Stdout
from envix.config.config import Config
from envix.exception import EnvixLoadEnvsError
from envix.loader import load_envs

OutputFormat = Literal["dotenv", "json"]


class Args(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    config_file: Path | None
    output_file: TextIOWrapper | None
    format: OutputFormat

    @field_validator("output_file", mode="before")
    @classmethod
    def validate_output_file(
        cls, output_file: TextIOWrapper | Stdout
    ) -> TextIOWrapper | None:
        return None if isinstance(output_file, Stdout) else output_file


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
        default=None,
    )

    parser.add_argument(
        "--output-file",
        "-o",
        help="output file path.",
        type=FileType("w"),
        default=Stdout(),
    )

    parser.add_argument(
        "--format",
        "-f",
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
                    f"{envname}={pipes.quote(secret.get_secret_value())}"
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
