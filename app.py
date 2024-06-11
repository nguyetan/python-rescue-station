from flask import Flask, jsonify, request
from flask_cors import CORS
import os

import services.firebase

from controllers.auth import auth
from controllers.feedback import feedback
from controllers.users import usersController

from dotenv import load_dotenv

from lib.find_stations import find_stations_LSCP, find_stations_PCenter

load_dotenv(".env")

app = Flask(__name__)
CORS(app, origins=['http://127.0.0.1:*', 'https://nguyetan.github.io/*', 'http://localhost:*'], supports_credentials=True)

@app.route('/' , methods=['GET'])
def hello():
    return 'This is the main page!'

@app.route('/auth' , methods=['POST'])
def authRequest():
    try:
        req = request.get_json()
        res = auth(req)
        return jsonify(res)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/findLSCP' , methods=['POST'])
def findLSCP():
    req = request.get_json()
    res = find_stations_LSCP(req['data'])
    return jsonify(res)

@app.route('/findPCenter' , methods=['POST'])
def findPCenter():
    req = request.get_json()
    res = find_stations_PCenter(req['data'])
    return jsonify(res)

@app.route('/feedback' , methods=['POST'])
def feedbackControl():
    req = request.get_json()
    res = feedback(req)
    return jsonify(res)

@app.route('/user' , methods=['POST'])
def userControl():
    req = request.get_json()
    res = usersController(req)
    return jsonify(res)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5013))
    app.run(host='0.0.0.0', port=port)