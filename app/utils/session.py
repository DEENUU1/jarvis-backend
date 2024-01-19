import uuid


def generate_unique_session() -> str:
    return uuid.uuid4().hex
