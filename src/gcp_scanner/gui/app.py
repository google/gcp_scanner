"""
The entry point for the visualization tool.

This module is responsible for starting the flask server and serving the
static files for the GUI.
"""

from flask import Flask
from flask import send_file, url_for

app = Flask(__name__)

@app.route("/")
def home():
  return send_file(url_for("static/index.html"))

def main():
  app.run(debug=False)

if __name__ == "__main__":
  main()
