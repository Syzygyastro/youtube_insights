# app.py
import os
from flask import Flask, session, redirect, url_for
from flask_cors import CORS
from config import DevelopmentConfig
from controllers.auth_controller import auth_bp
from controllers.data_controller import data_bp


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object(DevelopmentConfig)
app.secret_key = app.config['SECRET_KEY']

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Register blueprints
app.register_blueprint(auth_bp)
# app.register_blueprint(data_bp)
app.register_blueprint(data_bp)

@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('data.dashboard'))

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
