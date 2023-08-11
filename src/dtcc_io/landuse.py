from dtcc_model.landuse import Landuse, LanduseClasses
from dtcc_model import proto
from pathlib import Path
import fiona
import shapely.geometry
from .logging import info, warning, error
from . import generic
from enum import Enum, auto


class LanduseDatasource(Enum):
    LM = auto()
    OSM = auto()
    NONE = auto()


LM_landuse_map = {
    "VATTEN": LanduseClasses.WATER,
    "SKOGLÖV": LanduseClasses.FOREST,
    "SKOGSMARK": LanduseClasses.FOREST,
    "SKOGBARR": LanduseClasses.FOREST,
    "ODLÅKER": LanduseClasses.FARMLAND,
    "ÅKERMARK": LanduseClasses.FARMLAND,
    "ODLFRUKT": LanduseClasses.FARMLAND,
    "ÖPMARK": LanduseClasses.GRASS,
    "BEBLÅG": LanduseClasses.URBAN,
    "BEBHÖG": LanduseClasses.URBAN,
    "BEBSLUT": LanduseClasses.URBAN,
    "BEBIND": LanduseClasses.INDUSTRIAL,
}

LM_landuse_fn = lambda x: LM_landuse_map.get(x, LanduseClasses.URBAN)

landuse_mappings = {
    LanduseDatasource.LM: LM_landuse_fn,
    LanduseDatasource.OSM: None,
    LanduseDatasource.NONE: lambda x: LanduseClasses.URBAN,
}


def _load_proto_landuse(filename):
    landuse = Landuse()
    landuse.from_proto(filename.read_bytes())
    return landuse


def _load_fiona(
    filename,
    landuse_field="DETALJTYP",
    landuse_datasource=LanduseDatasource.LM,
    landuse_mapping_fn=None,
    **kwargs,
):
    if landuse_mapping_fn is None:
        landuse_mapping_fn = landuse_mappings.get(landuse_datasource)
    if landuse_mapping_fn is None:
        warning(f"Landuse mapping function not found, using default")
        landuse_mapping_fn = landuse_mappings[LanduseDatasource.NONE]
    info(f"Loading landuse from {filename}")
    if not filename.is_file():
        raise FileNotFoundError(f"File {filename} not found")
    Landuses = []
    with fiona.open(filename, "r") as src:
        for s in src:
            geom_type = s["geometry"]["type"]
            if geom_type == "Polygon":
                landuse = Landuse()
                landuse.footprint = shapely.geometry.shape(s["geometry"])
                landuse.landuse = landuse_mapping_fn(s["properties"][landuse_field])
                landuse.properties = s["properties"]
                Landuses.append(landuse)
            if geom_type == "MultiPolygon":
                for idx, polygon in enumerate(
                    list(shapely.geometry.shape(s["geometry"]).geoms)
                ):
                    # make each polygon its own building
                    landuse = Landuse()
                    landuse.footprint = polygon
                    landuse.landuse = landuse_mapping_fn(s["properties"][landuse_field])
                    landuse.properties = s["properties"]
                    Landuses.append(landuse)
    return Landuses


def load(
    filename,
    landuse_field="DETALJTYP",
    landuse_datasource: LanduseDatasource = LanduseDatasource.LM,
    landuse_mapping_fn=None,
) -> Landuse:
    """
    Load the land use data from a shapefile and return a `Landuse` object.

    Args:
        filename (str): The path to the shapefile.
        landuse_field (str): The name of the field containing the land use type (default "DETALJTYP").
        landuse_datasource (LanduseDatasource): The data source of the land use data (default LanduseDatasource.LM).
        landuse_mapping_fn (callable): A function to map from a land use attibute string to land use types (default None).

    Returns:
        Landuse: A `Landuse` object representing the land use data loaded from the shapefile.
    """
    filename = Path(filename)
    return generic.load(
        filename,
        "landuse",
        Landuse,
        _load_formats,
        landuse_field="DETALJTYP",
        landuse_datasource=LanduseDatasource.LM,
        landuse_mapping_fn=None,
    )


def _save_proto_landuse(landuse, filename):
    filename.write_bytes(landuse.to_proto().SerializeToString())


def save(landuse, filename):
    filename = Path(filename)
    return generic.save(landuse, filename, "landuse", _save_formats)


def list_io():
    return generic.list_io("pointcloud", _load_formats, _save_formats)


def print_io():
    generic.print_io("pointcloud", _load_formats, _save_formats)


_load_formats = {
    Landuse: {
        ".pb": _load_proto_landuse,
        ".pb2": _load_proto_landuse,
        ".shp": _load_fiona,
        ".geojson": _load_fiona,
        ".json": _load_fiona,
        ".gpkg": _load_fiona,
    }
}

_save_formats = {
    Landuse: {
        ".pb": _save_proto_landuse,
        ".pb2": _save_proto_landuse,
    }
}
