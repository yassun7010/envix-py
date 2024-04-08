from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from envix._helper import DOLLAR_ENVNAME_PATTERN, ENVNAME_PATTERN

from ._common import OverwriteType


class LocalEnvsV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Annotated[
        Literal["Local"],
        Field(title="ローカルに設定された環境変数を利用することを明示するための設定。"),
    ]
    items: Annotated[
        dict[
            Annotated[
                str,
                Field(pattern=ENVNAME_PATTERN),
            ],
            Annotated[
                str,
                Field(title="値を読み取る環境変数名。", pattern=DOLLAR_ENVNAME_PATTERN),
            ],
        ]
        | list[Annotated[str, Field(pattern=ENVNAME_PATTERN)]],
        Field(title="ローカルから読み取る環境変数名のリスト。"),
    ]

    overwrite: OverwriteType = True

    @property
    def _items(self) -> dict[str, str]:
        if isinstance(self.items, list):
            return {envname: envname for envname in self.items}

        else:
            return {
                envname: envvar.strip("$") for envname, envvar in self.items.items()
            }
