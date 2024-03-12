import json
from pathlib import Path

from dtcc_model import City
from dtcc_model import Surface, MultiSurface, Mesh, Building, BuildingPart
import numpy as np


def to_cityjson_multisurface(multisurface: MultiSurface, vertices, scale: float):
    vert_offset = len(vertices)
    boundaries = []
    for surface in multisurface.surfaces:
        vert_offset = len(vertices)
        boundary = []
        v = np.round(surface.vertices * scale).astype(int)
        vertices += v.tolist()
        boundary.append(list(range(vert_offset, len(vertices))))
        boundaries.append(boundary)

    cityjson_multisurface = {
        "type": "MultiSurface",
        "boundaries": boundaries,
    }
    return cityjson_multisurface


def to_cityjson(city: City, scale: float = 0.001):
    pass
    cityjson = {
        "type": "CityJSON",
        "version": "2.0",
        "transform": {"scale": [scale, scale, scale], "translate": [0.0, 0.0, 0.0]},
        "CityObjects": {},
        "vertices": [],
    }

    scale = 1 / scale
    vertices = []

    for obj in city.children[Building]:
        cityjson["CityObjects"][obj.id] = {
            "type": "Building",
            "geometry": [],
        }
        for part in obj.children[BuildingPart]:
            cityjson["CityObjects"][part.id] = {
                "type": "BuildingPart",
                "geometry": [],
            }
            for surface in part.children[Surface]:
                cityjson["CityObjects"][part.id]["geometry"].append(
                    to_cityjson_surface(surface, scale)
                )
            for multisurface in part.children[MultiSurface]:
                cityjson["CityObjects"][part.id]["geometry"].append(
                    to_cityjson_multisurface(multisurface, scale)
                )


def save(city: City, path: Path):
    """Save a city to a file.

    Args:
        city (City): The city to save.
        path (str or Path): Path to the file.
    """
    cj = to_cityjson(city)
    path = Path(path)
    if path.suffix == ".json":
        with open(path, "w") as file:
            json.dump(cityjson.dump(city), file, indent=2)
    else:
        raise ValueError(f"Unknown file format: {path.suffix}")
