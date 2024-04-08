from typing import Annotated

from pydantic import Field


OverwriteType = Annotated[
    bool,
    Field(title="既に設定済みの環境変数を上書きするかどうか。"),
]
