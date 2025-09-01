from json_reader.modern_reader import new_configuration_from_json, NewConfiguration
import json
import dataclasses


def test_config_inout(tmp_path):
    config = NewConfiguration(
        size=100,
        name="Test",
        simulation=True,
        path="data/somewhere",
        duration=10.0,
    )

    filename = tmp_path / "test.json"
    with filename.open("w") as f:
        json.dump(dataclasses.asdict(config), f)

    config2 = new_configuration_from_json(filename)

    assert config == config2
