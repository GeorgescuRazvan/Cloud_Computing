import json

def is_valid_book_payload(data):
    """
    Validates the book JSON payload.
    If data is a single book (dict), validate normally.
    If data is a list, validate each book in the list.
    """
    if isinstance(data, dict):  # Single book validation
        return (
            "title" in data and bool(data["title"]) and
            "author" in data and bool(data["author"]) and
            ("description" not in data or isinstance(data["description"], str))
        )
    
    if isinstance(data, list):  # Multiple books validation
        return all(is_valid_book_payload(book) for book in data)
    
    return False

def read_request_body(handler):
    length = int(handler.headers.get("Content-Length", 0))
    if length > 0:
        body = handler.rfile.read(length)
        return json.loads(body.decode("utf-8"))
    return {}
