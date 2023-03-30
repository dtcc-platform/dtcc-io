from google.protobuf.json_format import MessageToJson

def protobuf_to_json(pb_object,path, *args, **kwargs ):
    with open(path, "w") as f:
        f.write(MessageToJson(pb_object))
