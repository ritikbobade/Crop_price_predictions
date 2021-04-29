from flask import Flask, render_template, request
from keras import backend as K

from flask import *
from cropclimate import climate

app = Flask(__name__,template_folder='template')
K.clear_session()


@app.route('/')
def climate_index():
    return render_template('climate_index.html')


@app.route('/', methods=['POST','GET'])
def climate_result():
    if request.method == 'POST':
        climate_result = request.form
        output=climate(climate_result)
        print(output)
        return render_template("climate_result.html",result=climate_result,output=output)


if __name__ == '__main__':
    app.run(debug=True)