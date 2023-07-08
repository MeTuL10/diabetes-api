from flask import Flask, render_template, redirect, url_for,request
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
    
    gender = le1.transform(user_input['gender'])
    age = user_input['age']
    hypertension = user_input['hypertension']
    heart_disease = user_input['heart_disease']
    smoking_history = le2.transform(user_input['smoking_history'])
    bmi = user_input['bmi']
    HbA1c_level= user_input['HbA1c_level']
    blood_glucose_level= user_input['blood_glucose_level']
    u_input = [[gender,age,hypertension,heart_disease,smoking_history,bmi,HbA1c_level,blood_glucose_level]]
    #classes = np.array(['setosa', 'versicolor', 'virginica'])
    output = model.predict_classes(u_input)
    if output>0.1:
        return "you have diabetes"
    else:
        return "you dont have diabetes"

app = Flask(__name__)
# Configure a secret SECRET_KEY
#app.config['SECRET_KEY'] = '6c6722beeac20a0d45f7e977'
#CSRFProtect(app)
# Loading the model and scaler
predictor = load_model('models\\diabetes_predictor')
#flower_scaler = joblib.load(“iris_scaler.pkl”)
# Now create a WTForm Class

#gender age	hypertension heart_disease smoking_history bmi HbA1c_level blood_glucose_level diabetes

# class DiabetesForm(FlaskForm):
#     gender= StringField('gender')
#     age = StringField('age')
#     hypertension = StringField('hypertension')
#     heart_disease = StringField('heart_disease')
#     smoking_history = StringField('smoking_history')
#     bmi = StringField('bmi')
#     HbA1c_level = StringField('HbA1c_level')
#     blood_glucose_level = StringField('blood_glucose_level')
#     submit = SubmitField('Analyze')
u_input={}
@app.route('/', methods=['GET', 'POST'])
def index():
    global u_input
    if request.method=="POST":
        u_input['gender'] = request.form.get("gender")
        u_input['age'] = request.form.get("age")
        u_input['hypertension'] = request.form.get("hypertension")
        u_input['heart_disease'] = request.form.get("heart_disease")  
        u_input['smoking_history'] = request.form.get("smoking_history")
        u_input['bmi'] = request.form.get("bmi")
        u_input['HbA1c_level'] = request.form.get("HbA1c_level")
        u_input['blood_glucose_level'] = request.form.get("blood_glucose_level")
        print("a")
        return redirect(url_for('prediction'))
        #prediction()
    return render_template('index.html')
@app.route('/prediction')
def prediction():
    global u_input
    user_input = {}
    user_input['gender'] = str(u_input['gender'])
    user_input['age'] = float(u_input['age'])
    user_input['hypertension'] = int(u_input['hypertension'])
    user_input['heart_disease'] = int(u_input['heart_disease'])
    user_input['smoking_history'] = str(u_input['smoking_history'])
    user_input['bmi'] = float(u_input['bmi'])
    user_input['HbA1c_level'] = float(u_input['HbA1c_level'])
    user_input['blood_glucose_level'] = int(u_input['blood_glucose_level'])
    print(user_input)
    results = return_prediction(predictor,user_input)
    return render_template('prediction.html',results=results)

if __name__ == '__main__':
    app.run(debug=True)