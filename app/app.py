from flask import Flask, render_template
# from .cache_setup import cache
from .urls import register_routes

app = Flask(__name__, template_folder='templates', static_folder='static')

# cache.init_app(app)

register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)