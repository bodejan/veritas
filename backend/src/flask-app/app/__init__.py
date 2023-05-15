from flask import Flask
from flask_cors import CORS  # Import the CORS extension

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

# Configurations
app.config.from_object('config.Config')

# Register routes, do not remove
from app import routes


