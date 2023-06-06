from application import app
from flask import render_template , request, flash  , redirect , url_for , json, jsonify
from application.forms import PredictionForm , SignUpForm, LoginForm
from application import model , manager
from application import db
from application.models import Prediction , User
from datetime import datetime
import pandas as pd 


from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import login_user , logout_user , login_required , current_user

@manager.user_loader
def loader(userid):
    return User.query.get(int(userid))



@app.route('/hello')
def hello_world():
    return "<h1> Hello World </h1>"




# def add_entry(new_entry):
#     try:
#         db.session.add(new_entry)
#         db.session.commit()
#         return new_entry.id
#     except Exception as error:
#         db.session.rollback()
#         flash(error,"danger")
# def get_entries():
#     try:
#     # entries = Entry.query.all() # version 2
#         entries =db.session.execute(db.select(Entry).order_by(Entry.id)).scalars()
#         return entries
#     except Exception as error:
#         db.session.rollback()
#         flash(error,"danger")
#         return 0

# @app.route('/')
# @app.route('/index')
# @app.route('/home')
# def index_page():
#     form1 = PredictionForm()
#     return render_template("index.html", form=form1, title=
#     "Enter Iris Parameters" , entries = get_entries()  , iris_type = iris_type) 


@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    return render_template('index.html' , title = 'Predicting Your Health Insurance')

@app.route('/predict', methods=['GET','POST'])
@login_required
def predict():
    form = PredictionForm()
    print(form.data)
    if request.method == 'POST':
        if form.validate_on_submit():
            print('validated')
            age = int(form.age.data)
            diabetes = int(form.diabetes.data)
            bp = int(form.bp.data)
            transplants =int(form.transplants.data)
            chronic =int(form.chronic.data )
            height =float(form.height.data)
            weight =float(form.weight.data )
            allergy =int(form.allergy.data) 
            cancer= int(form.cancer.data )
            noSurgery=int( form.noSurgery.data )
            df = pd.DataFrame([[age ,   diabetes , bp , transplants  , chronic,height , weight  , allergy ,cancer , noSurgery ]]  , 
                              columns= ['Age',	'Diabetes'	,'BloodPressureProblems',	'AnyTransplants',	'AnyChronicDiseases',	'Height',	'Weight',	'KnownAllergies'	,'HistoryOfCancerInFamily'	,'NumberOfMajorSurgeries' ]  )
            df['bmi'] =df.Weight / ((df.Height/100)**2 )
            df.drop(columns = [ 'Height'], inplace = True)
            result = model.predict(df)
            print(result)
            userid = current_user.id  
            
            result = result[0]*0.017
            
            
            
            
            try:
                    
                newpred = Prediction(
                    diabetes = diabetes , 
                    bp = bp , 
                    transplants = transplants   ,
                    chronic = chronic , 
                    height = height , 
                    weight = weight , 
                    allergy = allergy ,
                    cancer = cancer , 
                    age = age , 
                    predictedPremium = result ,
                    userid = userid  , 
                    noSurgery = noSurgery, 
                    predicted_on = datetime.utcnow()
                    
                )
                db.session.add(newpred)
                db.session.commit()
                flash(f"Prediction: ${round(result, 2 )}  per year","success")
            except Exception as e:
                print(e)
                db.session.rollback() 
                flash("Error, unable to save prediction", 'danger')
            
            
        else:
            print('errors' , form.errors)
            flash('Error, cannot proceed with prediction' , 'danger')
    return render_template("prediction.html", form=form, title="Predict Insurance Premium" , index = True )



@app.route('/predhistory', methods=['GET'])
@login_required
def predicthist():
    
    
    userid = current_user.id
    predictions = Prediction.query.filter_by( userid = userid).all()

    return render_template("predictionhistory.html"  , predictions = predictions, title="Predict Insurance Premium" , index = True )




@app.route('/logout' , methods = ['GET' , 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/login')
    
    
    
@app.route('/signup', methods=['GET','POST'] )
def signup():
    form = SignUpForm()
    
    
    if request.method == 'POST':
        if form.validate_on_submit():
            password = form.password.data
            username = form.username.data
            
            
            
            try:
                newuser = User(username  = username, password= password)
                db.session.add(newuser)
                db.session.commit()
                login_user(newuser)#login user after account created successfully
                return redirect('/')
            except:
                flash('Error! Username/email Already exists. Please choose a different one' , 'danger')
                
            

        else:
            flash('Error, Unable to Sign Up' , 'danger')
    return render_template("signup.html", form=form, title="Sign Up" , index = True )




@app.route('/login', methods=['GET','POST'] )
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username = form.username.data ).first()
            print(user)
            if user:
        
                if check_password_hash(user.password , form.password.data):
                    print('login')
                    login_user(user)
                    return redirect('/')
                else:
                    flash('Wrong password' , 'danger')
                    
            else:
                flash('User does not exist' , 'danger')
                
        else:
            flash('Error, Unable to login' , 'danger')
    return render_template("login.html", form=form, title="Sign Up" , index = True )




@app.route('/api/getpred/<uid>', methods = ['GET'])
def getpred(uid):
    data = request.args.get('username')
    id =uid
    
    try:
        
        pred = Prediction.query.filter_by(id = id ).first()
        finaldata = pred.__dict__
        del finaldata['_sa_instance_state']
        print(finaldata)
        
        return {'status' :'successful' , 'data' : finaldata}
    except:
        return {'status' :'unccessful'} , 400
    
    
    
    
    






@app.route('/api/storeprediction', methods = ['POST'])
def storepredictionjson():
    data = request.get_json()
    age = data['age']
    diabetes = data['diabetes']
    bp = data['bp']
    transplants =data['transplants']
    chronic =data['chronic']
    height =data['height']
    weight =data['weight']
    allergy =data['allergy']
    cancer= data['cancer']
    noSurgery=data['noSurgery']
    userid = data['userid']
    pred = data['predictedPremium']
    current = datetime.utcnow()
    newpred = Prediction(
            diabetes = diabetes , 
            bp = bp , 
            transplants = transplants   ,
            chronic = chronic , 
            height = height , 
            weight = weight , 
            allergy = allergy ,
            cancer = cancer , 
            age = age , 
            predictedPremium = pred,
            userid = userid  , 
            noSurgery = noSurgery, 
            predicted_on =current
            
        )
    

    try:
        db.session.add(newpred)
        db.session.commit()
        
        assert newpred.diabetes == diabetes 
        assert newpred.bp == bp 
        assert newpred.transplants == transplants
        assert newpred.chronic == chronic 
        assert newpred.height == height 
        assert newpred.weight == weight
        assert newpred.allergy == allergy
        assert newpred.cancer == cancer
        assert newpred.age == age
        assert newpred.predictedPremium == pred
        assert newpred.userid == userid
        assert newpred.noSurgery == noSurgery
        assert newpred.predicted_on == current
        
        return {'id' : newpred.id }
    except Exception as e:
        print(e)
        db.session.rollback() 
        return {'status' :'fail'}, 400 



    

@app.route('/api/adduser', methods = ['POST'])
def storeuser():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    
    try:
        
    
        newuser = User( username = username , password = password)
        
        db.session.add(newuser)
        db.session.commit() 
        
        assert newuser.username ==  username 
        assert check_password_hash(newuser.password, password )
        return {'status' :newuser.id}
    except Exception as e:
        print(e)
        db.session.rollback()
        return {'status' : 'fail'} , 400
    



    
    

@app.route('/api/getprediction', methods=['POST'])
def predict_model():
    data = request.get_json()
    age = data['age']
    diabetes = data['diabetes']
    bp = data['bp']
    transplants =data['transplants']
    chronic =data['chronic']
    height =data['height']
    weight =data['weight']
    allergy =data['allergy']
    cancer= data['cancer']
    noSurgery=data['noSurgery']
    current = datetime.utcnow()
    # print(form.data)
    # print('validated')
    # age = int(form.age.data)
    # diabetes = int(form.diabetes.data)
    # bp = int(form.bp.data)
    # transplants =int(form.transplants.data)
    # chronic =int(form.chronic.data )
    # height =float(form.height.data)
    # weight =float(form.weight.data )
    # allergy =int(form.allergy.data) 
    # cancer= int(form.cancer.data )
    # noSurgery=int( form.noSurgery.data )
    df = pd.DataFrame([[age ,   diabetes , bp , transplants  , chronic,height , weight  , allergy ,cancer , noSurgery ]]  , 
                        columns= ['Age',	'Diabetes'	,'BloodPressureProblems',	'AnyTransplants',	'AnyChronicDiseases',	'Height',	'Weight',	'KnownAllergies'	,'HistoryOfCancerInFamily'	,'NumberOfMajorSurgeries' ]  )
    df['bmi'] =df.Weight / ((df.Height/100)**2 )
    df.drop(columns = [ 'Height'], inplace = True)
    result = model.predict(df)
    return {'predicted' : result[0] }