from dtcc_model import City
from pathlib import Path
from .cityjson import cityjson
import json


def load(path):
    """Load a city from a file.

    Args:
        path (str or Path): Path to the file.

    Returns:
        City: The loaded city.
    """
    path = Path(path)
    if path.suffix == ".json":
        with open(path, "r") as file:
            data = json.load(file)
        if data.get("type") == "CityJSON":
            return cityjson.load(path)
        else:
            raise ValueError(f"{path} is not a CityJSON file")
    else:
        raise ValueError(f"Unknown file format: {path.suffix}")
