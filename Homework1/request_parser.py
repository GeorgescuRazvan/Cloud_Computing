import re
from urllib.parse import urlparse

def parse_path(path):
    """
    Parses the request path to extract the resource and an optional id.
    Example:
        /books        -> returns ("books", None)
        /books/123    -> returns ("books", "123")
    """
    parsed = urlparse(path).path.rstrip("/")
    match = re.match(r"^/books(?:/([^/]+))?$", parsed)
    if match:
        book_id = match.group(1) if match.group(1) else None
        return "books", book_id
    return None, None