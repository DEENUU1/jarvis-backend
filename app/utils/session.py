import uuid


def generate_unique_session():
    return uuid.uuid4().hex
