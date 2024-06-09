from flask import Flask, jsonify, request
from flask_cors import CORS
import os

import services.firebase

from controllers.auth import auth

from dotenv import load_dotenv

from lib.find_stations import find_stations_LSCP, find_stations_PCenter

load_dotenv(".env")

app = Flask(__name__)
CORS(app, origins=['http://127.0.0.1:*', 'https://nguyetan.github.io/rescue-station'], supports_credentials=True)

@app.route('/' , methods=['GET'])
def hello():
    return 'This is the main page!'

@app.route('/auth' , methods=['POST'])
def authRequest():
    req = request.get_json()
    res = auth(req)
    return jsonify(res)

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5013))
    app.run(host='0.0.0.0', port=port)