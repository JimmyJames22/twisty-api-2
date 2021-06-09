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
    # create object to hold request params
    params = {
        'client_id': request.args.get('client_id'),
        'origin': request.args.get('origin'),
        'destination': request.args.get('destination'),
        'mode': request.args.get('mode'),
        'avoid': request.args.get('avoid')
    }

    # check for missing params
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

    # write back missing params
    if param_error:
        error_string = {'Method': 'POST', 'Error': {'Missing': errors}}
        resp = Response(str(error_string), 404)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    # create routes if no missing params
    else:
        map_master = MapMaster(params)
        resp = map_master.get_route()
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@app.route('/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user():
    # create object to hold request params
    params = {
        'client_id': request.args.get('client_id'),
        'firstname': request.args.get('firstname'),
        'lastname': request.args.get('lastname'),
        'email': request.args.get('email'),
        'old_email': request.args.ger('old_email'),
        'password': request.args.get('password'),
        'old_password': request.args.get('old_password'),
        'phone': request.args.get('phone'),
        'addresses': request.args.get('addresses')
    }

    # handle GET request
    if request.method == 'GET':
        # check for missing params
        errors = []
        param_error = False
        if params['email'] is None:
            errors.append("email")
            param_error = True
        if params['password'] is None:
            errors.append("password")
            param_error = True

        # write back missing params
        if param_error:
            error_string = {'Method': 'POST', 'Error': {'Missing': errors}}
            resp = Response(str(error_string), 404)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        # create routes if no missing params
        else:
            user_obj = User(params)
            resp = user_obj.get_user()
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp

    # handle POST request
    elif request.method == 'POST':
        # check for missing params
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

        # write back missing params
        if param_error:
            error_string = {'Method': 'POST', 'Error': {'Missing': errors}}
            resp = Response(str(error_string), 404)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        # create routes if no missing params
        else:
            user_obj = User(params)
            resp = user_obj.post_user()
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp

    # handle PUT request
    elif request.method == 'PUT':
        # check for missing params
        errors = []
        param_error = False
        if params['old_email'] is None:
            errors.append("old_email")
            param_error = True
        if params['old_password'] is None:
            errors.append("old_password")
            param_error = True

        # write back missing params
        if param_error:
            error_string = {'Method': 'POST', 'Error': {'Missing': errors}}
            resp = Response(str(error_string), 404)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        # create routes if no missing params
        else:
            resp_error = {'Method': 'PUT', 'Error': {'Missing': ['client_id']}}
            resp = Response(str(resp_error), 404)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp

    # handle DELETE request
    elif request.method == 'DELETE':
        # check for missing params
        errors = []
        param_error = False

        if params['email'] is None:
            errors.append("email")
            param_error = True
        if params['password'] is None:
            errors.append("password")
            param_error = True

        # write back missing params
        if param_error:
            error_string = {'Method': 'POST', 'Error': {'Missing': errors}}
            resp = Response(str(error_string), 404)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        # create routes if no missing params
        else:
            resp_error = {'Method': 'DELETE', 'Error': {'Missing': ['client_id']}}
            resp = Response(str(resp_error), 404)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp


if __name__ == '__main__':
    app.run(ssl_context=('ssl/twistyroads.tk-crt.pem', 'ssl/twistyroads.tk-key.pem'), host='0.0.0.0', port=443 )
# ewregu
