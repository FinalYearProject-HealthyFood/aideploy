import os
from flask import Flask, request, Response
from flask_restful import Resource, Api
from flask_cors import CORS

from json import dumps
from flask import jsonify
from werkzeug.utils import secure_filename
import random
import requests
import pandas as pd
import numpy as np
from model import *
import requests
import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from pulp import *
import numpy as np
UPLOAD_FOLDER = 'image'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)
CORS(app)
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getData(data_api):
    response = requests.get(data_api)
    data_json = response.json()
    data = pd.DataFrame(data_json)
    data = data.replace('na',np.nan)
    data = data.fillna(0)
    return data

class Tracks(Resource):
    def get(self):
        result = "ttt"
        return jsonify(result)

class dietoptimize(Resource):
    def post(self):
        if request.method == 'POST':
            # if 'calories' not in request.data:
            #     result = "No file part"
            #     return jsonify(result)
            # data = request.get_json()
            data = request.get_json()
            calories = data.get('calories')
            ingredient = data.get('ingredient')
            # calories = request.args.get('calories')
            # ingredient = request.args.get('ingredient')
            data_api = "http://127.0.0.1:8000/api/ingredients/datatoai"
            data = getData(data_api)
            data_ingredient = pd.DataFrame((ingredient))
            print("thisiss",data_ingredient['name'])
            result = DietModel(data,int(calories),data_ingredient)
            # print(data[data["OptimalValue"]!= 0])
            # return jsonify(data[data["OptimalValue"]!= 0].to_json(orient = 'columns'))
            # finalresult =  Response(data[data["OptimalValue"]!= 0].to_json(orient="records"), mimetype='application/json')
            # finalresult =  Response(result.to_json(orient="records"), mimetype='application/json')
            finalresult =  jsonify(result.to_dict(orient='records'))
            finalresult.headers.add('Access-Control-Allow-Origin', '*')
            # finalresult.headers["Content-Type"] = "application/json"
            # finalresult.headers.add('Access-Control-Allow-Origin', '*')
            # print("this is",calories,(data_ingredient))
            return finalresult
            # return calories
            # return Response(data[data["OptimalValue"]!= 0].to_json(orient="records"), mimetype='application/json')

api.add_resource(Tracks, '/tracks')
api.add_resource(dietoptimize, '/diet-list')
if __name__ == '__main__':
     app.run()