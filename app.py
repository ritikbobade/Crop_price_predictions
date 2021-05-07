from flask import Flask, render_template, request
from keras import backend as K

from flask import *
from cropmodel import prediction
from cropclimate import climate 
from historic import history

app = Flask(__name__, template_folder='template')
K.clear_session()


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


if __name__ == '__main__':
    app.run(debug=True)
    
