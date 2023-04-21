# Copyright(C) 2023 Anders Logg and Dag Wästberg
# Licensed under the MIT License

from google.protobuf.json_format import MessageToJson

from .logging import info, error


def protobuf_to_json(pb_object, path, *args, **kwargs):
    with open(path, "w") as f:
        f.write(MessageToJson(pb_object))


def save_to_pb(pb_mesh, path):
    with open(path, "wb") as f:
        f.write(pb_mesh.SerializeToString())
