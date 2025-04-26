from flask import Flask
from app.urls import register_routes
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

register_routes(app)

if __name__ == '__main__':
    # Use PORT environment variable if set, default to 5000 for local development
    port = int(os.getenv('PORT', 5000))
    # Bind to 0.0.0.0 to make the app externally accessible
    app.run(host='0.0.0.0', port=port, debug=True)