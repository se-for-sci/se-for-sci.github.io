# Original, raw implementation

import json
import dataclasses


@dataclasses.dataclass
class NewConfiguration:
    size: int
    name: str
    simulation: bool
    path: str
    duration: float


def new_configuration_from_json(filename):
    """Read a JSON file and return the contents as a Configuration object."""

    with open(filename, encoding="utf-8") as f:
        json_dict = json.load(f)

    # Optional, but protects against extra keys in the JSON file
    config_dict = {
        f.name: json_dict[f.name] for f in dataclasses.fields(NewConfiguration)
    }

    return NewConfiguration(**config_dict)
