from flask import Flask, Response
from routes.index import index_app
from routes.spotify import auth_app
from dotenv import load_dotenv
from secrets import token_hex
import os

load_dotenv()
app = Flask(__name__)
app.register_blueprint(index_app, url_prefix='/')
app.register_blueprint(auth_app, url_prefix='/spotify')

if os.getenv('ENV') == 'prod':
    app.secret_key = token_hex() #sessions will restart on app reset
else:
    app.secret_key = "development" #session will stay

@app.errorhandler(404)
def page_not_found(error):
    d = {'status': 404, 'message': 'Resource not found.'}
    return d, 404

app.run(port=8080)