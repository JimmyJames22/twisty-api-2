from flask import Flask
from flask import Response
from flask import request
from flask_restful import Api, Resource, reqparse
import mysql.connector

from user import User

hostName = "0.0.0.0"
serverPort = 3000

con = mysql.connector.connect(
    host="24.60.153.154",
    user="root",
    database="users"
)

print("MySQL connected")

app = Flask(__name__)
api = Api(app)


@app.route('/user', methods=['GET', 'POST', 'PUT'])
def getUser():
    parser = reqparse.RequestParser()
    parser.add_argument("client_id")
    parser.add_argument('firstname')
    parser.add_argument('lastname')
    parser.add_argument('email')
    parser.add_argument('password')
    parser.add_argument('phone')
    parser.add_argument('addresses')
    params = parser.parse_args()
    print(params)

    if request.method == 'GET':
        if params['client_id']:
            user = User(params)
            user.print_user()
            resp = user.get_user(con)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp


if __name__ == '__main__':
    app.run(ssl_context=('Ssl/cert.crt', 'Ssl/key.pem'), host='0.0.0.0', port=443)
# ewregu
