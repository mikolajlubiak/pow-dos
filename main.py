import http.server
from http import HTTPStatus
import json
import random
import string
import hashlib

challenge = ''.join(random.choices(string.ascii_lowercase, k=64))
difficulty = 4

# Define the handler for GET and POST requests
class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Set response status code and headers
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Read and serve an HTML file
        with open('index.html', 'r') as file:
            html_content = file.read()

        html_content = html_content.replace('EXAMPLE', challenge)
        html_content = html_content.replace('DIFFICULTY', str(difficulty))

        self.wfile.write(html_content.encode())

    def do_POST(self):
        # Set response status code and headers
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # Read and process POST data as JSON
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_params = json.loads(post_data)

            # Process the POST request and send a response
            msg = challenge + str(post_params['nonce'])
            response_message = 'bad'
            if (
                    post_params['challenge'] == challenge and
                    post_params['hash'].startswith('0'*difficulty)
                    ):
                if hashlib.sha512(msg.encode()).hexdigest() == post_params['hash']:
                    response_message = 'good'

            self.wfile.write(response_message.encode('utf-8'))
        except Exception as e:
            error_message = f'Error processing POST request: {str(e)}'
            self.wfile.write(error_message.encode('utf-8'))

# Create an HTTP server that listens on port 8000
httpd = http.server.HTTPServer(('localhost', 8000), MyHandler)
print('Server started on http://localhost:8000')

# Start the server
httpd.serve_forever()
