import json

def set_headers(handler, code, content_type="application/json"):
    handler.send_response(code)
    handler.send_header("Content-Type", content_type)
    handler.end_headers()

def send_json_response(handler, data):
    handler.wfile.write(json.dumps(data).encode())