from flask import Flask
from flask import Response
from flask import request
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
import mysql.connector
from urllib.parse import parse_qs

from user import User
from mapmaster import MapMaster

app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route('/route', methods=['GET'])
def route():
    params = {
        'client_id': request.args.get('client_id'),
        'origin': request.args.get('origin'),
        'destination': request.args.get('destination'),
        'mode': request.args.get('mode'),
        'avoid': request.args.get('avoid')
    }

    errors = []
    param_error = False

    if params['client_id'] is None:
        errors.append("client_id")
        param_error = True
    if params['origin'] is None:
        errors.append("origin")
        param_error = True
    if params['destination'] is None:
        errors.append("destination")
        param_error = True

    if param_error:
        error_string = {'Method': 'POST', 'Error': {'Missing': errors}}
        resp = Response(str(error_string), 404)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        map_master = MapMaster(params)
        resp = map_master.get_route()
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@app.route('/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user():
    params = {
        'client_id': request.args.get('client_id'),
        'firstname': request.args.get('firstname'),
        'lastname': request.args.get('lastname'),
        'email': request.args.get('email'),
        'password': request.args.get('password'),
        'phone': request.args.get('phone'),
        'addresses': request.args.get('addresses')
    }

    if request.method == 'GET':
        if params['client_id'] is None:
            resp_error = {'Method': 'GET', 'Error': {'Missing': ['client_id']}}
            resp = Response(str(resp_error), 404)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            user = User(params)
            resp = user.get_user()
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
    elif request.method == 'POST':
        errors = []
        param_error = False

        if params['firstname'] is None:
            errors.append("firstname")
            param_error = True
        if params['lastname'] is None:
            errors.append("lastname")
            param_error = True
        if params['email'] is None:
            errors.append('email')
            param_error = True
        if params['password'] is None:
            errors.append('password')
            param_error = True
        if params['addresses'] is None:
            errors.append('addresses')
            param_error = True
        if param_error:
            error_string = {'Method': 'POST', 'Error': {'Missing': errors}}
            resp = Response(str(error_string), 404)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            user = User(params)
            resp = user.post_user()
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
    elif request.method == 'PUT':
        if params['client_id']:
            user = User(params)
            resp = user.put_user()
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            resp_error = {'Method': 'PUT', 'Error': {'Missing': ['client_id']}}
            resp = Response(str(resp_error), 404)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
    elif request.method == 'DELETE':
        if params['client_id']:
            user = User(params)
            resp = user.delete_user()
            return resp
        else:
            resp_error = {'Method': 'DELETE', 'Error': {'Missing': ['client_id']}}
            resp = Response(str(resp_error), 404)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp


if __name__ == '__main__':
    app.run(ssl_context=('ssl/twistyroads.tk-crt.pem', 'ssl/twistyroads.tk-key.pem'), host='0.0.0.0', port=443 )
# ewregu
