import os
from textwrap import dedent

import pytest
from envix.cli.app import App

from tests.config_builder import ConfigV1Builder


class TestCliAppInjectCommand:
    def test_inject_command_with_help(self):
        with pytest.raises(SystemExit):
            App.run(["inject", "--help"])

    def test_inject_command_with_config(
        self,
        config_v1_builder: ConfigV1Builder,
        capfd: pytest.CaptureFixture[str],
    ):
        os.environ.clear()

        with (
            config_v1_builder.chain()
            .add_envs("FOO", "1234567890")
            .add_envs("BAR", "abcdefghijklmn")
            .build_file()
        ) as config_file:
            App.run(["inject", "--config-file", config_file.name, "env"])

        out, err = capfd.readouterr()
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
