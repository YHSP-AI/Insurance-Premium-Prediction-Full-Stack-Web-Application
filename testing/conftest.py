import pytest 
import flask_login 
from application import app, db , models
from werkzeug.security import generate_password_hash , check_password_hash
from collections import namedtuple

# @pytest.fixture()
# def new_application():
#     print('called')
#     from application import app , db 
#     yield app , db
    
    
    
@pytest.fixture()
def application_client( ):
    # application, db .= new_application
    from application import app , db  , models

    with app.app_context():
        user = models.User(username = 'valid1.email@gmail.com' , password = ('password'))#create a random user so that it is possible to interact with database

        db.session.add(user)
        db.session.commit()
        
            
        yield   dict(context = app.test_client() , userid = user.id ) 
        
        
        db.session.query(models.User).delete()
        db.session.query(models.Prediction ).delete() 
        db.session.commit()






    
# @pytest.fixture()
# def application_client_retrieve( ):
#     # application, db .= new_application
#     from application import app , db  , models

#     with app.app_context():
#         user = models.User(username = 'valid1.email@gmail.com' , password = ('password'))#create a random user so that it is possible to interact with database

#         db.session.add(user)
#         db.session.commit()
        
#         newpredictionrow = 
        
            
#         yield   dict(context = app.test_client() , userid = user.id ) 
        
        
#         db.session.query(models.User).delete()
#         db.session.query(models.Prediction ).delete() 
#         db.session.commit()
