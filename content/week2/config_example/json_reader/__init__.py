# Original, raw implementation

import json


class Configuration:
    def __init__(self, *, size, name, simulation, path, duration):
        self.size = size
        self.name = name
        self.simulation = simulation
        self.path = path
        self.duration = duration


def configuration_from_json(filename):
    """Read a JSON file and return the contents as a Configuration object."""

    with open(filename, encoding="utf-8") as f:
        json_dict = json.load(f)

    return Configuration(
        size=json_dict["size"],
        name=json_dict["name"],
        simulation=json_dict["simulation"],
        path=json_dict["path"],
        duration=json_dict["duration"],
    )
