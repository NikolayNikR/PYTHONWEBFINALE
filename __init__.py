from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your-secret-key'
app.config['ROOMS_FILE'] = 'trade.json'


from app import routes