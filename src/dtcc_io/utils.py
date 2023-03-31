from google.protobuf.json_format import MessageToJson

def protobuf_to_json(pb_object,path, *args, **kwargs ):
    with open(path, "w") as f:
        f.write(MessageToJson(pb_object))


def save_to_pb(pb_mesh, path):
    with open(path, "wb") as f:
        f.write(pb_mesh.SerializeToString())