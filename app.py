from flask import Flask, render_template, request
from keras import backend as K

from flask import *
from cropmodel import prediction
from cropclimate import climate 

app = Flask(__name__, template_folder='template')
K.clear_session()


@app.route('/')
def index():
    return render_template('index.html')
    # request.method and request.form
    # nmpy_list from form
    # output = model(nmpy_list)


@app.route('/', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        print(result)
        output = prediction(result)
        print(output)
        return render_template("result.html", result=result, output=output)

@app.route('/climate')
def climate_index():
    return render_template('climate_index.html')


@app.route('/climate', methods=['POST','GET'])
def climate_result():
    if request.method == 'POST':
        climate_result = request.form
        output=climate(climate_result)
        print(output)
        return render_template("climate_result.html",result=climate_result,output=output)        

if __name__ == '__main__':
    app.run(debug=True)
    
