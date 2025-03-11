import json
from http.server import BaseHTTPRequestHandler
from request_parser import parse_path
from response_helper import set_headers, send_json_response
import storage_manager
from validators import is_valid_book_payload, read_request_body

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        resource, book_id = parse_path(self.path)
        if resource != "books":
            set_headers(self, 404)
            send_json_response(self, {"error": "Resource not found"})
            return

        if book_id:
            # GET /books/{id}
            book = storage_manager.find_book_by_id(book_id)
            if book:
                set_headers(self, 200)
                send_json_response(self, book)
            else:
                set_headers(self, 404)
                send_json_response(self, {"error": "Book not found"})
        else:
            # GET /books
            books = storage_manager.list_books()
            set_headers(self, 200)
            send_json_response(self, books)

    def do_POST(self):
        resource, book_id = parse_path(self.path)
        if resource != "books":
            set_headers(self, 404)
            send_json_response(self, {"error": "Resource not found"})
            return

        try:
            data = read_request_body(self)
        except Exception:
            set_headers(self, 400)
            send_json_response(self, {"error": "Invalid JSON data"})
            return

        if not is_valid_book_payload(data):
            set_headers(self, 400)
            send_json_response(self, {"error": "Invalid book data"})
            return

        if book_id:
            # POST /books/{id} creates a new book with specified id (if not exists)
            if storage_manager.find_book_by_id(book_id):
                set_headers(self, 409)
                send_json_response(self, {"error": "Book with given id already exists"})
            else:
                set_headers(self, 404)
                send_json_response(self, {"error": "Cannot create book with custom id"})
        else:
            # POST /books creates a new book with auto-generated id
            new_id = storage_manager.generate_new_id()
            data["_id"] = new_id
            storage_manager.create_book_with_id(new_id, data)
            set_headers(self, 201)
            send_json_response(self, {"message": "Book created", "book": data})

    def do_PUT(self):
        resource, book_id = parse_path(self.path)
        if resource != "books":
            set_headers(self, 404)
            send_json_response(self, {"error": "Resource not found"})
            return

        try:
            data = read_request_body(self)
        except Exception:
            set_headers(self, 400)
            send_json_response(self, {"error": "Invalid JSON data"})
            return

        if not is_valid_book_payload(data):
            set_headers(self, 400)
            send_json_response(self, {"error": "Invalid book data"})
            return

        if book_id:
            # PUT /books/{id} updates an existing book or creates one if not found
            book = storage_manager.find_book_by_id(book_id)
            if book:
                storage_manager.update_book(book_id, data)
                set_headers(self, 200)
                send_json_response(self, {"message": "Book updated"})
            else:
                set_headers(self, 404)
                send_json_response(self, {"error": "Book id not found"})
        else:
            # PUT /books replaces the entire collection (expects a list of books)
            if not isinstance(data, list):
                set_headers(self, 400)
                send_json_response(self, {"error": "Expected a list of books"})
                return
            storage_manager.replace_all_books(data)
            set_headers(self, 200)
            send_json_response(self, {"message": "Book collection replaced"})

    def do_DELETE(self):
        resource, book_id = parse_path(self.path)
        if resource != "books":
            set_headers(self, 404)
            send_json_response(self, {"error": "Resource not found"})
            return

        if book_id:
            # DELETE /books/{id}
            book = storage_manager.find_book_by_id(book_id)
            if book:
                storage_manager.delete_book(book_id)
                set_headers(self, 200)
                send_json_response(self, {"message": "Book deleted"})
            else:
                set_headers(self, 404)
                send_json_response(self, {"error": "Book not found"})
        else:
            # DELETE /books
            storage_manager.delete_all_books()
            set_headers(self, 200)
            send_json_response(self, {"message": "All books deleted"})

    def log_message(self, format, *args):
        # Suppress default logging
        pass
