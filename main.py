from app import app
from waitress import serve
serve(app, host='0.0.0.0', port=5000, url_scheme='https')
