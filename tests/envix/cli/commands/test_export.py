from textwrap import dedent

import pytest
from envix.cli.app import App

from tests.config_builder import ConfigV1Builder


class TestCliAppExportCommand:
    def test_export_command_with_help(self):
        with pytest.raises(SystemExit):
            App.run(["export", "--help"])

    def test_export_command_with_config(
        self,
        config_v1_builder: ConfigV1Builder,
        capsys: pytest.CaptureFixture[str],
    ):
        with (
            config_v1_builder.chain()
            .add_envs("FOO", "1234567890")
            .add_envs("BAR", "abcdefghijklmn")
            .build_file()
        ) as config_file:
            App.run(["export", "--config-file", config_file.name])

        out, err = capsys.readouterr()
        assert (
            out
            == dedent(
                """
                FOO=1234567890
                BAR=abcdefghijklmn
                """
            ).lstrip()
        )
        assert err == ""
