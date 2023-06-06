import pytest

import json


@pytest.mark.parametrize(
    'data' , [(dict(
        age = 20, 
        diabetes = True , 
            bp = False , 
            transplants = False   ,
            chronic = False , 
            height = 150 , 
            weight = 60 , 
            allergy = False ,
            cancer = True, 
            predictedPremium = 20000,
            noSurgery = 2, 
            
    )), 
       (dict(
        age = 30, 
        diabetes = False , 
            bp = False , 
            transplants = True   ,
            chronic = False , 
            height = 145 , 
            weight = 80 , 
            allergy = False ,
            cancer = True, 
            predictedPremium = 10000,
            noSurgery = 3, 
            
    ) )]
)
def test_insert_prediction(application_client  , data):
    context = application_client['context']
    userid = application_client['userid'] 
    newdata = data.copy() 
    
    newdata['userid'] = userid 
    
    response = context.post('/api/storeprediction' , data=json.dumps(newdata),content_type="application/json")
    
    assert response.status_code == 200
    assert  isinstance(json.loads(response.get_data(as_text= True))["id"] , int )
    


@pytest.mark.xfail(strict=True)#Expected Fail email
@pytest.mark.parametrize(
    'data' , [(dict(
        age = 20, 
        diabetes = True , 
            bp = False , 
            transplants = False   ,
            chronic = False , 
            height = 120 , #invalid height 
            weight = 60 , 
            allergy = False ,
            cancer = True, 
            predictedPremium = 20000,
            noSurgery = 2, 
            
    )), 
       (dict(
        age = 20, 
        diabetes = False , 
        bp = False , 
        transplants = True   ,
        chronic = False , 
        height = 150 , 
        weight = 60 , 
        allergy = False ,
        cancer = True, 
        predictedPremium = 10000,
        noSurgery = 10, #invalid number of surgery
            
    ) ) , ((dict(
        age = 20, 
        diabetes = False , 
        bp = False , 
        transplants = True   ,
        chronic = False , 
        height = 150 , 
        weight = 10 , #invalid weight
        allergy = False ,
        cancer = True, 
        predictedPremium = 10000,
        noSurgery = 2, 
            
    ) )) , 
    ((dict(
        age = 10, #invalid age
        diabetes = False , 
        bp = False , 
        transplants = True   ,
        chronic = False , 
        height = 150 , 
        weight = 60 , 
        allergy = False ,
        cancer = True, 
        predictedPremium = 10000,
        noSurgery = 2, 
            
    ) )), 
     ((dict(
        age = 10, #invalid age
        diabetes = None , # None values 
        bp = False , 
        transplants = True   ,
        chronic = None , 
        height = 150 , 
        weight = 60 , 
        allergy = None ,
        cancer = True, 
        predictedPremium = 10000,
        noSurgery = 2, 
            
    ) ))]
)
def test_insert_prediction_fail(application_client, data ):
    test_insert_prediction(application_client, data)
    
    





@pytest.mark.parametrize(#expected pass user
    'data' , [(
        dict(
            username = 'valid.email@gmail.com' , 
            password = 'vvvvvvvvalidpasswordlength8'
        )) , 
        (dict(
             username = 'another.valid.email@gmail.com' , 
            password = 'anothervalidpasswordlength8'
        )), (dict(
            username = 'yhang.21@ichat.sp.edu.sg',
            password = 'paswordlength8'
        ))]
)
def test_insert_user(application_client,data): 
    context = application_client['context']
    userid = application_client['userid'] 
    response = context.post('/api/adduser', data = json.dumps( data) 
                 ,content_type="application/json")
    assert response.status_code == 200
    assert  isinstance(json.loads(response.get_data(as_text= True))["status"] , int )
    
    


@pytest.mark.xfail(strict=True)#Expected Fail email
@pytest.mark.parametrize(
    'data' , [(
        dict(
            username = 'invalidemail' , 
            password = 'aas'
        )) , 
        (dict(
             username = '' , 
            password = ''
        ))]
)
def test_insert_user_fail(application_client, data ):
    test_insert_user(application_client, data)
    
    
    
    
    

@pytest.mark.parametrize(
    'data' , [(dict(
        age = 20, 
        diabetes = True , 
            bp = False , 
            transplants = False   ,
            chronic = False , 
            height = 150 , 
            weight = 60 , 
            allergy = False ,
            cancer = True, 
            predictedPremium = 20000,
            noSurgery = 2, 
            
    )), 
       (dict(
        age = 30, 
        diabetes = False , 
            bp = False , 
            transplants = True   ,
            chronic = False , 
            height = 145 , 
            weight = 80 , 
            allergy = False ,
            cancer = True, 
            predictedPremium = 10000,
            noSurgery = 3, 
            
    ) )]
)
def test_get_prediction(application_client  , data  , create_pred = True):
    context = application_client['context']
    userid = application_client['userid'] 
    newdata = data.copy() 
    
    newdata['userid'] = userid 
    if create_pred == True:
        response = context.post('/api/storeprediction' , data=json.dumps(newdata),content_type="application/json")
        
        newid = json.loads(response.get_data(as_text= True))["id"]
    else:
        newid = 0
    response = context.get(f'/api/getpred/{newid}' )
    assert response.status_code == 200 
    responsedata = json.loads(response.get_data(as_text= True))
    assert responsedata['data']
    responsedata = responsedata['data']
    print(responsedata)
    assert responsedata['age'] == data['age']
    assert responsedata['diabetes'] == data['diabetes']
    assert responsedata['transplants'] == data['transplants']
    assert responsedata['chronic'] == data['chronic']
    assert responsedata['height'] == data['height']
    assert responsedata['allergy'] == data['allergy']
    assert responsedata['cancer'] == data['cancer']
    assert responsedata['predictedPremium'] == data['predictedPremium']
    assert responsedata['noSurgery'] == data['noSurgery']
    
    
    
    
@pytest.mark.xfail(strict=True)
def test_fail_get_prediction(application_client     ):
    test_get_prediction(application_client  , data = None   , create_pred = False)
    
    
    
@pytest.mark.parametrize(
    'data',[(dict(
        age = 20, 
        diabetes = True , 
            bp = False , 
            transplants = False   ,
            chronic = False , 
            height = 150 , 
            weight = 60 , 
            allergy = False ,
            cancer = True, 
            noSurgery = 2, 
            
    ))], 
    [ 
     [(dict(
        age = 20, 
        diabetes = True , 
            bp = False , 
            transplants = False   ,
            chronic = False , 
            height = 150 , 
            weight = 60 , 
            allergy = False ,
            cancer = True, 
            noSurgery = 2, 
            
    ))]]
)
def test_model_consistency(application_client , data):
    #test if model return same prediction everytime same input given
    
    context = application_client['context']
    userid = application_client['userid'] 
    response = context.post('/api/getprediction', data = json.dumps( data) ,content_type="application/json")
    initial_pred  = json.loads(response.get_data(as_text= True))
    for _ in range(50):
        response = context.post('/api/getprediction', data = json.dumps( data) ,content_type="application/json")
        
        newpred = json.loads(response.get_data(as_text= True))
        
        assert newpred['predicted'] == initial_pred['predicted']
        