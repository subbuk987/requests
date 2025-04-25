import json
from http.server import HTTPServer, BaseHTTPRequestHandler


class MyHandler(BaseHTTPRequestHandler):
    """
    Custom HTTP request handler to process POST requests for appending data to a file.
    """

    def do_POST(self):
        """
        Handles HTTP POST requests.

        - Expects 'Content-Type: application/json' header.
        - Endpoint must be '/append'.
        - JSON payload must include:
            {
                "filename": "<file_path>",
                "data": "<text_to_append>"
            }
        - Appends the text to the file.
        - Sends custom response headers and JSON body as response.
        """
        content_length = int(self.headers.get("Content-Length"))
        sent_data = self.rfile.read(content_length)

        if self.headers.get("Content-Type") == "application/json" and self.path == "/append":
            post_data = json.loads(sent_data.decode())
            filename = post_data.get("filename")
            data = post_data.get("data")

            if filename and data:
                try:
                    with open(filename, "a") as file:
                        file.write("\n" + data)

                    response = {
                        "Status": "Success",
                        "User": self.headers.get("X-User"),
                        "Summary": f"Data appended to {filename}"
                    }
                    self.send_response(200)
                    self.send_header("X-Server", "localhost")
                    self.send_header("X-File-Appended", f"{filename}")
                    self.end_headers()

                except FileNotFoundError:
                    response = {
                        "Status": "Error",
                        "User": self.headers.get("X-User"),
                        "Summary": f"File: {filename} not Found..."
                    }
                    self.send_response(404)
                    self.send_header("X-Server", "localhost")
                    self.send_header("X-File-Appended", "Failure")
                    self.end_headers()
            else:
                response = {
                    "Status": "Error",
                    "User": self.headers.get("X-User"),
                    "Summary": "Invalid Data"
                }
                self.send_response(404)
                self.send_header("X-Server", "localhost")
                self.send_header("X-File-Appended", "Failure")
                self.end_headers()

            self.wfile.write(json.dumps(response).encode())
        else:
            self.wfile.write(json.dumps("Invalid Content Type! Expected JSON.").encode())


if __name__ == "__main__":
    """
    Main entry point of the server script.

    - Binds the HTTP server to localhost on port 8000.
    - Starts the server and listens for requests until interrupted (Ctrl+C).
    - Gracefully shuts down on KeyboardInterrupt.
    """
    server_address = ("localhost", 8000)
    server = HTTPServer(server_address, MyHandler)

    print("Server started. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer shutting down gracefully...")
        server.server_close()
