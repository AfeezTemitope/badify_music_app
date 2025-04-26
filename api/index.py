from app.app import app
from wsgi import application

# Vercel serverless function handler
def handler(request):
    return application(request.environ, lambda status, headers: request.response.start(status, headers))