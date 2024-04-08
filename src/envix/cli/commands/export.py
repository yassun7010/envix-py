from argparse import ArgumentParser, FileType, _SubParsersAction
from pathlib import Path
from typing import Any, cast

from pydantic import BaseModel


class Args(BaseModel):
    command: str
    args: list[str]
    config_file: Path


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
        "command",
        metavar="COMMAND",
    )

    parser.add_argument(
        "--config-file",
        metavar="CONFIG_FILE",
        help="config file path.",
        type=Path,
        default="envix.toml",
    )

    parser.add_argument(
        "--output-file",
        "-o",
        help="output file path.",
        type=FileType("w"),
        default=None,
    )

    parser.set_defaults(handler=lambda space: export_command(Args(**vars(space))))


def export_command(args: Args) -> None:
    raise NotImplementedError()
