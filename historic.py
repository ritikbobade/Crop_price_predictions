import numpy as np
import keras
import tensorflow as tf
from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json

K.clear_session()

def history(input_numbers):
    
    input_list=[]
    input_list.append(input_numbers['Year'])
    input_list.append(input_numbers['Month'])
    input_list.append(90)
    if (input_numbers['Crop']==["Arhar"]):
        input_list.append(1)
        input_list.append(0)
    else:
        input_list.append(0)
    print(input_list)

    input_list = np.array(input_list)
    input_list = input_list.reshape((1, 4))
    input_list = np.matrix(input_list)

    json_file = open('C:/Users/ritik/Mini Project/modelhs.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    global graph
    graph = tf.compat.v1.get_default_graph()
    with graph.as_default():
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights("C:/Users/ritik/Mini Project/modelhs.h5")

        loaded_model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mean_absolute_error'])

        values = loaded_model.predict(input_list)
        del input_list
    keras.backend.clear_session()
    return values            
