"""
The entry point for the visualization tool.

This module is responsible for starting the HTTP server and serving the
static files for the GUI.
"""

import argparse
import http.server
import socketserver
import os


def main():
    parser = argparse.ArgumentParser(
        description='GCP Scanner GUI',
        usage='python3 %(prog)s -p 8080')
    parser.add_argument(
        '-p',
        '--port',
        default=8080,
        type=int,
        dest='port',
        help='Port to serve the GUI on')
    args = parser.parse_args()

    # change directory to the GUI directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/static')

    with socketserver.TCPServer(("", args.port), http.server.SimpleHTTPRequestHandler) as httpd:
        print('\033[92m' + 'Serving at: ' + '\033[94m' + 'http://localhost:' + str(args.port) + '\033[0m')

        httpd.serve_forever()


if __name__ == '__main__':
    main()