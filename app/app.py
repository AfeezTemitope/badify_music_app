from flask import Flask
from app.urls import register_routes

app = Flask(__name__, template_folder='templates', static_folder='static')

register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)