from flask import Flask, render_template, json,request,url_for,session,redirect
from keras import backend as K
from flask_pymongo import PyMongo
from pymongo import MongoClient
from wtforms import Form, BooleanField, StringField, PasswordField, validators
import bcrypt
from flask import *
from flask import session
from cropmodel import prediction
from cropclimate import climate
from historic import history

app = Flask(__name__, template_folder='template')
K.clear_session()

app.config['MONGO_DBNAME'] = 'user'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/user'

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')
    # request.method and request.form
    # nmpy_list from form
    # output = model(nmpy_list)

@app.route('/geo')
def geographic():
    return render_template('geography.html')

    
@app.route('/geo', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        print(result)
        outputn = prediction(result)
        output=str(outputn).lstrip('[').rstrip(']')
        return render_template("result.html", result=result, output=output)

@app.route('/climate')
def climate_index():
    return render_template('climate.html')


@app.route('/climate', methods=['POST','GET'])
def climate_result():
    if request.method == 'POST':
        climate_result = request.form
        outputn=climate(climate_result)
        output1= outputn + 100
        output=str(output1).lstrip('[').rstrip(']')
        return render_template("result.html",result=climate_result,output=output)        

@app.route('/historic')
def historic():
    return render_template('previousdataset.html')

@app.route('/historic', methods=['POST','GET'])
def his_result():
    if request.method == 'POST':
        his_result = request.form
        outputn=history(his_result)
        output1= outputn + 100
        output=str(output1).lstrip('[').rstrip(']')
        return render_template("result.html",result=climate_result,output=output)


@app.route('/login')
def login_index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('login.html')


@app.route('/login1', methods=['POST','GET'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})
    print(request.form['username'])
    logged_user = request.form['username']
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return render_template("index.html")

    return render_template("popup.html")

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            msg = '{ "html":"ok"}'
            msghtml = json.loads(msg)
            # return msg["html"]
            return msghtml["html"]
        else:
            msg = '{ "html":"user"}'
            msghtml = json.loads(msg)
            return msghtml["html"]

        # return 'That username already exists!'

    return render_template('signup.html')


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
    
