from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import NumberRange
import numpy as np 
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder
from flask_wtf.csrf import CSRFProtect

#parameters:
#gender age	hypertension heart_disease smoking_history bmi HbA1c_level blood_glucose_level diabetes
def return_prediction(model,user_input):    
    f=open("encodedlabels.txt","r")
    txt=f.readline()
    le1=LabelEncoder()
    c1=txt.split(", ")
    c1[-1]=c1[-1][:-1]
    txt=f.readline()
    le2=LabelEncoder()
    c2=txt.split(", ")
    c2[-1]=c2[-1]
    le1.classes_=c1
    le2.classes_=c2
    
    #gender = le1.transform(user_input['gender'])
    gender=c1.index(user_input["gender"])
    age = user_input['age']
    hypertension = user_input['hypertension']
    heart_disease = user_input['heart_disease']
    #smoking_history = le2.transform(user_input['smoking_history'])
    smoking_history=c2.index(user_input["smoking_history"])
    bmi = user_input['bmi']
    HbA1c_level= user_input['HbA1c_level']
    blood_glucose_level= user_input['blood_glucose_level']
    input = [[gender,age,hypertension,heart_disease,smoking_history,bmi,HbA1c_level,blood_glucose_level]]
    #classes = np.array(['setosa', 'versicolor', 'virginica'])
    output = model.predict(input)
    if output>0.1:
        return "you have diabetes"
    else:
        return "you dont have diabetes"

app = Flask(__name__)
# Configure a secret SECRET_KEY
app.config['SECRET_KEY'] = '6c6722beeac20a0d45f7e977'
CSRFProtect(app)
# Loading the model and scaler
predictor = load_model('models\\diabetes_predictor')
#flower_scaler = joblib.load(“iris_scaler.pkl”)
# Now create a WTForm Class

#gender age	hypertension heart_disease smoking_history bmi HbA1c_level blood_glucose_level diabetes

class DiabetesForm(FlaskForm):
    gender= StringField('gender')
    age = StringField('age')
    hypertension = StringField('hypertension')
    heart_disease = StringField('heart_disease')
    smoking_history = StringField('smoking_history')
    bmi = StringField('bmi')
    HbA1c_level = StringField('HbA1c_level')
    blood_glucose_level = StringField('blood_glucose_level')
    submit = SubmitField('Analyze')
 
@app.route('/', methods=['GET', 'POST'])
def index():
    form = DiabetesForm()
    if form.is_submitted():
        print("submitted")

    if form.validate():
        print("valid")

    print(form.errors)
    if form.validate_on_submit():
        session['gender'] = form.gender.data
        session['age'] = form.age.data
        session['hypertension'] = form.hypertension.data
        session['heart_disease'] = form.heart_disease.data  
        session['smoking_history'] = form.smoking_history.data 
        session['bmi'] = form.bmi.data 
        session['HbA1c_level'] = form.HbA1c_level.data 
        session['blood_glucose_level'] = form.blood_glucose_level.data 
        return redirect(url_for('prediction'))
        #prediction()
    return render_template('index.html', form=form)
@app.route('/prediction')
def prediction():
    user_input = {}
    user_input['gender'] = str(session['gender'])
    user_input['age'] = float(session['age'])
    user_input['hypertension'] = int(session['hypertension'])
    user_input['heart_disease'] = int(session['heart_disease'])
    user_input['smoking_history'] = str(session['smoking_history'])
    user_input['bmi'] = float(session['bmi'])
    user_input['HbA1c_level'] = float(session['HbA1c_level'])
    user_input['blood_glucose_level'] = int(session['blood_glucose_level'])
    results = return_prediction(predictor,user_input)
    return render_template('prediction.html',results=results)

if __name__ == '__main__':
    app.run(debug=True)