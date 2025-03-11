import json

def is_valid_book_payload(data):
    """
    Validates the book JSON payload.
    Requires 'title' and 'author' to be non-empty.
    """
    if not isinstance(data, dict):
        return False
    if "title" not in data or not data["title"]:
        return False
    if "author" not in data or not data["author"]:
        return False
    if "description" in data and not isinstance(data["description"], str):
        return False
    return True

def read_request_body(handler):
    length = int(handler.headers.get("Content-Length", 0))
    if length > 0:
        body = handler.rfile.read(length)
        return json.loads(body.decode("utf-8"))
    return {}