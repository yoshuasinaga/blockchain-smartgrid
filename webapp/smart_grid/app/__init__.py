from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from web3 import Web3

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)

from app import routes
from app.prediction import schedule_predictions

# Initialize data prediction
w3 = Web3(Web3.HTTPProvider(app.config['WEB3_CONSUMERS_URI']))
user_list = w3.eth.accounts
schedule_predictions(w3, user_list)