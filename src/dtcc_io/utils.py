# Copyright(C) 2023 Anders Logg and Dag Wästberg
# Licensed under the MIT License

from google.protobuf.json_format import MessageToJson

from .logging import info, warning, error


def get_epsg(fiona_crs):
    try:
        # old style crs
        crs = fiona_crs["init"]
    except KeyError:
        # new style crs
        crs = fiona_crs.to_epsg()
        if crs is None:
            # see https://gis.stackexchange.com/questions/326690/explaining-pyproj-to-epsg-min-confidence-parameter
            crs = fiona_crs.to_epsg(20)
            if crs is None:
                warning("Cannot determine crs, assuming EPSG:3006")
                crs = "3006"
        crs = f"EPSG:{crs}"
    return crs


def protobuf_to_json(pb_object, path, *args, **kwargs):
    with open(path, "w") as f:
        f.write(MessageToJson(pb_object, including_default_value_fields=True))


def save_to_pb(pb_mesh, path):
    with open(path, "wb") as f:
        f.write(pb_mesh.SerializeToString())
