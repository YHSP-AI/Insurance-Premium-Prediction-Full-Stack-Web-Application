from flask import Flask

import joblib 
from flask_sqlalchemy import SQLAlchemy
import sys
import os 
app = Flask(__name__)
this_dir = os.path.dirname(__file__) 
app.config.from_pyfile('config.cfg')


joblib_file = os.path.join(this_dir, "./static/InsurancePremiumPredictor")



app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy( session_options={

    'expire_on_commit': False

})


with app.app_context():
    db.init_app(app)
    from .models import Prediction , User 
    db.create_all()
    db.session.commit()
    print('Created Database!')
from flask_login import LoginManager
manager = LoginManager()
manager.init_app(app)

model = joblib.load(joblib_file)
from application import routes 