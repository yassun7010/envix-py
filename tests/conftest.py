from pytest import fixture

from tests.config_builder import ConfigV1Builder


@fixture
def config_v1_builder() -> ConfigV1Builder:
    return ConfigV1Builder()
