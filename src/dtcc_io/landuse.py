from dtcc_model.landuse import Landuse, LanduseClasses
from dtcc_model import proto
from pathlib import Path
import fiona
import shapely.geometry

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


def load(
    filename,
    landuse_field="DETALJTYP",
    landuse_map=LM_landuse_map,
    default_landuse=LanduseClasses.URBAN,
):
    filename = Path(filename)
    if not filename.is_file():
        raise FileNotFoundError(f"File {filename} not found")
    Landuses = []
    with fiona.open(filename, "r") as src:
        for s in src:
            geom_type = s["geometry"]["type"]
            if geom_type == "Polygon":
                landuse = Landuse()
                landuse.footprint = shapely.geometry.shape(s["geometry"])
                landuse.landuse = landuse_map.get(
                    s["properties"][landuse_field], default_landuse
                )
                landuse.properties = s["properties"]
                Landuses.append(landuse)
            if geom_type == "MultiPolygon":
                for idx, polygon in enumerate(
                    list(shapely.geometry.shape(s["geometry"]).geoms)
                ):
                    # make each polygon its own building
                    landuse = Landuse()
                    landuse.footprint = polygon
                    landuse.landuse = landuse_map[s["properties"][landuse_field]]
                    landuse.properties = s["properties"]
                    Landuses.append(landuse)
    return Landuses
