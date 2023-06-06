from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField , SelectField , IntegerField , StringField , PasswordField
from wtforms.validators import Length, InputRequired, ValidationError,NumberRange , Email  , EqualTo , Length

def length_validator(form, field):
    l = field.data
    print(field.data)
    if l == '':
        raise ValidationError("No Value Chosen")
    
    
class LoginForm(FlaskForm):
    username = StringField('Username (Username) \n Username must be an email' , validators = [InputRequired() , Email()])
    password = PasswordField("Password" , validators= [InputRequired()] )
    submit = SubmitField("Login")
    
class SignUpForm(FlaskForm):
    username = StringField('Username' , validators = [InputRequired() , Email()  ])
    password = PasswordField("Password" , validators= [InputRequired()] )
    confirmpassword = PasswordField("Password  Confirm" , validators= [InputRequired()  , EqualTo('password')] )
    submit = SubmitField("Sign Up")

    
    
    
    
    
class PredictionForm(FlaskForm):
    diabetes = SelectField('Do you have Diabetes?', choices=[('','') , (1, 'Yes'),(0, 'No' ) ], validators = [InputRequired() , length_validator])
    bp = SelectField('Do you have High/Low blood pressure?', choices=[('','') , (1, 'Yes'),(0, 'No')], validators = [InputRequired() , length_validator])
    transplants = SelectField('Have you received any transplants before?', choices=[('','') , (1, 'Yes'),(0, 'No')], validators = [InputRequired() , length_validator])
    chronic = SelectField('Do you suffer from any chrionic Diseases', choices=[('','') , (1, 'Yes'),(0, 'No')], validators = [InputRequired() , length_validator])
    height = FloatField('What is your height in cm', validators=[InputRequired(), NumberRange(145,188)])
    weight = FloatField('What is your weight in kg', validators=[InputRequired(), NumberRange(51,132)])
    allergy = SelectField('Do you have any allergies?', choices=[('','') , (1, 'Yes'),(0, 'No'), ('','')], validators = [InputRequired() , length_validator])
    cancer = SelectField('Do you have history of cancer in your family?', choices=[('','') , (1, 'Yes'),(0, 'No')]  , validators = [InputRequired() , length_validator])
    noSurgery = IntegerField('How many times have you performed major surgery', 
                             validators=[InputRequired(), NumberRange(0,3)])
    age = IntegerField("How old are you?",validators=[InputRequired(), NumberRange(18,66)])
    submit = SubmitField("Predict my Insurance Premium")