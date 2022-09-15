from json_reader import configuration_from_json, Configuration
import json

import pytest


def test_config1():
    config = configuration_from_json("tests/config1.json")

    assert isinstance(config, Configuration)

    assert config.size == 100
    assert config.name == "Test"
    assert config.simulation is True
    assert config.path == "data/somewhere"
    assert config.duration == 10.0


def test_make_config():
    config = Configuration(
        size=100,
        name="Test",
        simulation=True,
        path="data/somewhere",
        duration=10.0,
    )

    assert config.size == 100
    assert config.name == "Test"
    assert config.simulation is True
    assert config.path == "data/somewhere"
    assert config.duration == 10.0


def test_config_inout(tmp_path):
    config = Configuration(
        size=100,
        name="Test",
        simulation=True,
        path="data/somewhere",
        duration=10.0,
    )

    filename = tmp_path / "test.json"
    with filename.open("w") as f:
        json.dump(config.__dict__, f)

    config2 = configuration_from_json(filename)

    assert config.__dict__ == config2.__dict__


def test_extra_key(tmp_path):
    config = Configuration(
        size=100,
        name="Test",
        simulation=True,
        path="data/somewhere",
        duration=10.0,
    )

    filename = tmp_path / "test.json"
    with filename.open("w") as f:
        json.dump({**config.__dict__, "extra": "value"}, f)

    config2 = configuration_from_json(filename)

    assert config.__dict__ == config2.__dict__


def test_missing_key(tmp_path):
    config = Configuration(
        size=100,
        name="Test",
        simulation=True,
        path="data/somewhere",
        duration=10.0,
    )

    filename = tmp_path / "test.json"
    with filename.open("w") as f:
        json.dump({k: v for k, v in config.__dict__.items() if k != "name"}, f)

    with pytest.raises(KeyError):
        configuration_from_json(filename)
