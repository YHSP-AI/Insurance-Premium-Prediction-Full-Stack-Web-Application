from application import db
from flask_login import UserMixin
import re 
from werkzeug.security import generate_password_hash , check_password_hash

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
class User(UserMixin , db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable = False , unique = True)
    password = db.Column(db.String, nullable = False )
    
    def __init__(self, **data):
        self.username = data['username']
        if not re.fullmatch(regex, self.username):
            raise Exception('Username must be in email format')
        
        if len(data['password']) < 6:
            raise Exception('Password must be 6 characters long')
        
        
        self.username = data['username']
        
        data['password'] = generate_password_hash(data['password'])
        
         
        super().__init__(**data )
        
    
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    diabetes = db.Column( db.Boolean ,  nullable=False)
    bp = db.Column( db.Boolean ,  nullable=False)
    transplants = db.Column( db.Boolean ,  nullable=False)
    chronic  = db.Column( db.Boolean, nullable = False)
    height = db.Column(db.Float , nullable = False)
    weight = db.Column(db.Float, nullable = False)
    allergy = db.Column(db.Boolean, nullable = False)
    cancer = db.Column(db.Boolean , nullable = False)
    noSurgery = db.Column(db.Integer, nullable = False)
    age = db.Column(db.Integer , nullable = False )
    predictedPremium = db.Column(db.Float, nullable = False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id') , nullable = False)
    predicted_on = db.Column(db.DateTime, nullable=False)
    
    
    def __init__(self, **data):
        
        
        if data['age'] < 18 or data['age'] > 66:
            raise Exception("Age is out of bounds")
        
        if data['noSurgery'] < 0 or data['noSurgery'] > 3:
            raise Exception("noSurgery is out of bounds")
        
        if data['height'] < 145 or data['height'] > 188:
            raise Exception("height is out of bounds")
        
        if data['weight'] < 51 or data['weight'] > 132:
            raise Exception("weight is out of bounds")
        
        
        
        super().__init__(**data )
    # diabetes = SelectField('Do you have Diabetes?', choices=[('','') , (1, 'Yes'),(0, 'No' ) ], validators = [InputRequired() , length_validator])
    # bp = SelectField('Do you have High/Low blood pressure?', choices=[('','') , (1, 'Yes'),(0, 'No')], validators = [InputRequired() , length_validator])
    # transplants = SelectField('Have you received any transplants before?', choices=[('','') , (1, 'Yes'),(0, 'No')], validators = [InputRequired() , length_validator])
    # chronic = SelectField('Do you suffer from any chrionic Diseases', choices=[('','') , (1, 'Yes'),(0, 'No')], validators = [InputRequired() , length_validator])
    # height = FloatField('What is your height in cm', validators=[InputRequired(), NumberRange(1,200)])
    # weight = FloatField('What is your weight in kg', validators=[InputRequired(), NumberRange(1,200)])
    # allergy = SelectField('Do you have any allergies?', choices=[('','') , (1, 'Yes'),(0, 'No'), ('','')], validators = [InputRequired() , length_validator])
    # cancer = SelectField('Do you have history of cancer in your family?', choices=[('','') , (1, 'Yes'),(0, 'No')]  , validators = [InputRequired() , length_validator])
    # noSurgery = IntegerField('How many times have you performed major surgery', 
    #                          validators=[InputRequired(), NumberRange(1,100)])
    # age = FloatField("How old are you?",validators=[InputRequired(), NumberRange(1,100)])
    # submit = SubmitField("Predict my Insurance Premium")