from flask import Flask
from flask import Response
from flask import request
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
import mysql.connector
from urllib.parse import parse_qs

from user import User

app = Flask(__name__)
CORS(app)
api = Api(app)


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
        if params['client_id']:
            user = User(params)
            resp = user.get_user()
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            resp = Response('No client_id specified')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
    elif request.method == 'POST':
        errors = []
        param_error = False

        if params['firstname'] is None:
            errors.append("FIRSTNAME")
            param_error = True
        if params['lastname'] is None:
            errors.append("LASTNAME")
            param_error = True
        if params['email'] is None:
            errors.append('EMAIL')
            param_error = True
        if params['password'] is None:
            errors.append('PASSWORD')
            param_error = True
        if params['addresses'] is None:
            errors.append('ADDRESSES')
            param_error = True

        if param_error:
            error_string = "Missing: "
            for x in range(0, len(errors)):
                if x != len(errors) - 1:
                    errors[x] += ", "
                error_string += errors[x]

            resp = Response(error_string, 404)
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
            resp = Response('No client_id specified')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
    elif request.method == 'DELETE':
        if params['client_id']:
            user = User(params)
            resp = user.delete_user()
            return resp
        else:
            resp = Response('No client_id specified')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp


if __name__ == '__main__':
    app.run(ssl_context=('Ssl/cert.crt', 'Ssl/key.pem'), host='0.0.0.0', port=4443)
# ewregu
