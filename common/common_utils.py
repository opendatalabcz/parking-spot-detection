import base64


def serialize_bytes(bytes):
    return base64.encodebytes(bytes).decode("UTF-8")


def deserialize_bytes(src):
    return base64.decodebytes(src.encode("UTF-8"))
