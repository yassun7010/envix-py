from pathlib import Path

import pytest
from envix.config.config import Config
from envix.exception import EnvixConfigFileNotFound
from envix.loader import collect_secrets, load_secrets

from tests.config_builder import ConfigV1Builder


class TestV1Load:
    @pytest.mark.asyncio
    async def test_load_v1(
        self,
        config_builder: ConfigV1Builder,
        caplog: pytest.LogCaptureFixture,
    ):
        config = Config(config_builder.add_include("not_exists.yml").build())

        await collect_secrets(config)
        for record in caplog.records:
            assert isinstance(record.msg, EnvixConfigFileNotFound)

    @pytest.mark.asyncio
    async def test_load_sample(self, data_dir: Path):
        secrets, errors = await load_secrets(
            data_dir.joinpath("registered/envix_sample.yml")
        )

        assert not errors
        assert list(secrets.keys()) == ["SNOWFLAKE_ACCOUNT"]

    @pytest.mark.asyncio
    async def test_load_includes_sample(
        self,
        data_dir: Path,
        caplog: pytest.LogCaptureFixture,
    ):
        config_filepath = data_dir.joinpath("registered/envix_includes_sample.yml")
        secrets, errors = await load_secrets(config_filepath)

        assert not errors
        assert not caplog.records
        assert list(secrets.keys()) == ["SNOWFLAKE_ACCOUNT", "POSTGRES_ACCOUNT"]
