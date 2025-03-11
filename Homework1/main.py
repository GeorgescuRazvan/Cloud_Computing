from http.server import HTTPServer
from request_handler import RESTRequestHandler

def run(server_class=HTTPServer, handler_class=RESTRequestHandler, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting REST API server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()