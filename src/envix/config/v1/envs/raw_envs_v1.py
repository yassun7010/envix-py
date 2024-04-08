from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from envix._helper import ENVNAME_PATTERN

from ._common import OverwriteType


class RawEnvsV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Annotated[
        Literal["Raw"],
        Field(title="設定ファイルに直接記述する環境変数の設定。"),
    ]

    items: Annotated[
        dict[Annotated[str, Field(pattern=ENVNAME_PATTERN)], str],
        Field(title="直接記述する環境変数名と値の辞書。"),
    ]

    overwrite: OverwriteType = True
