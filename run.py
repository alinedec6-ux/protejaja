import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

from app import create_app

app = create_app()

if __name__ == "__main__":
    host = "0.0.0.0" if os.environ.get("DOCKER", "0") == "1" else "127.0.0.1"
    app.run(debug=True, host=host, port=5000)