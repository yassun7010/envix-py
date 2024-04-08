from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from envix._helper import ENVNAME_PATTERN

from ._common import OverwriteType


class GoogleCloudSecretManagerSecret(BaseModel):
    secret_id: str
    version: Annotated[int, Field(ge=1)] | Literal["latest"] = "latest"


class GoogleCloudSecretManagerEnvsV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["GoogleCloudSecretManager"]

    project_id: Annotated[
        str,
        Field(
            title="Google Cloud Platform のプロジェクトID。",
        ),
    ]

    items: dict[
        Annotated[str, Field(pattern=ENVNAME_PATTERN)],
        Annotated[
            str,
            Field(
                pattern=r"secrets/\w+/versions/([0-9]+|latest)",
                examples=["secrets/456/versions/789"],
            ),
        ]
        | GoogleCloudSecretManagerSecret,
    ]

    overwrite: OverwriteType = True

    @property
    def secret_items(self) -> dict[str, str]:
        items: dict[str, str] = {}
        for envname, secret in self.items.items():
            if isinstance(secret, str):
                items[envname] = f"projects/{self.project_id}/{secret}"
            elif isinstance(secret, GoogleCloudSecretManagerSecret):
                items[envname] = (
                    f"projects/{self.project_id}/secrets/{secret.secret_id}/versions/{secret.version}"
                )

        return items
