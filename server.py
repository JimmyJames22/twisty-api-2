from flask import Flask
from flask import request

from user import User

hostName = "0.0.0.0"
serverPort = 3000

con = mysql.connector.connect(
    host="localhost",
    user="root",
    database="users"
)

print("MySQL connected")

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user', methods=['GET', 'POST', 'PUT'])
def user():
    if request.method == 'GET':
        if request.form['client_id']:
            user = User(request.form)
            user.get_user(self, con)
        else:
            self.send_response(301)
            self.send_header("Content-type", "text/html")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes("No client_id", "utf-8"))
    elif request.method == 'POST':
        if not url_params.__contains__('firstname'):
            self.send_response(301)
            self.send_header("Content-type", "text/html")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes("No firstname", "utf-8"))
        elif not url_params.__contains__('lastname'):
            self.send_response(301)
            self.send_header("Content-type", "text/html")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes("No lastname", "utf-8"))
        elif not url_params.__contains__('email'):
            self.send_response(301)
            self.send_header("Content-type", "text/html")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes("No email", "utf-8"))
        elif not url_params.__contains__('password'):
            self.send_response(301)
            self.send_header("Content-type", "text/html")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes("No password", "utf-8"))
        elif not url_params.__contains__('addresses'):
            self.send_response(301)
            self.send_header("Content-type", "text/html")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes("No addresses", "utf-8"))
        else:
            user = User(url_params)
            user.print_user()
            user.post_user(self, con)
    elif request.method == 'PUT':
        if url_params.__contains__('client_id'):
            user = User(url_params)
            user.put_user(self, con)
        else:
            self.send_response(306)
            self.send_header("Content-type", "text/html")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes("No client_id", "utf-8"))


if __name__ == '__main__':
    app.run(ssl_context=('Ssl/cert.crt', 'Ssl/key.pem'))
# ewregu
