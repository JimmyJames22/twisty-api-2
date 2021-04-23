# ------- SQL STRUCTURE --------
# DB users
#   |-> useraddresses
#   |-> userhistory
#   |-> userlist
#   |-> userlogin
#   |-> usersettings
#
# ------- API STRUCTURE --------
# /user
#   |-> GET
#     |-> params: clientid (clientid, int)
#     |-> modify:
#     |-> use: db: user | table: userlist, useraddress, userlogin
#     |-> return: all data for the user
#   |-> POST
#     |-> params: firstname (string), lastname (string), email (string), password (string), phone (string) [optional], address (array of arrays  [["description", "streetAddress1", "streetAddress2", "city", "state", "zipcode"]])
#     |-> modify: db: users | table: userlist, useraddress, userlogin
#     |-> use: db: user | table: userlist, useraddress, userlogin
#     |-> return:
#   |-> PUT
#     |-> params:
# /user/login
#   |-> GET
#     |-> params: email (string), password (string)
#     |-> modify:
#     |-> use: db: user | table: userlogin
#     |-> return: string with value: "email", "password", or "success" to indicate error/success
# /user/display
#   |-> GET
#     |-> params: clientid (int)
#     |-> modify:
#     |-> use: db: user | table: userlogin
#     |-> return: string with value: "email", "password", or "success" to indicate error/success
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import mysql.connector
from user import User

hostName = "0.0.0.0"
serverPort = 3000

con = mysql.connector.connect(
    host="localhost",
    user="root",
    database="users"
)

print("MySQL connected")


class Client(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.end_headers()

    def do_GET(self):
        if self.path.__contains__('?'):
            url = self.path.split('?')
            url_path = url[0]
            url_params = parse_qs(url[1])
        else:
            self.send_response(300)
            self.send_header("Content-type", "text/html")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes("No params", "utf-8"))
            return

        if url_path == "/user":
            if url_params.__contains__('client_id'):
                user = User(url_params)
                user.get_user(self, con)
            else:
                self.send_response(301)
                self.send_header("Content-type", "text/html")
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(bytes("No client_id", "utf-8"))
        elif url_path == "/route":
            if not url_params.__contains__('origin'):
                self.send_response(301)
                self.send_header("Content-type", "text/html")
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(bytes("No origin", "utf-8"))
            if not url_params.__contains__('destination'):
                self.send_response(301)
                self.send_header("Content-type", "text/html")
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(bytes("No origin", "utf-8"))



    def do_POST(self):
        if self.path.__contains__('?'):
            url = self.path.split('?')
            url_path = url[0]
            url_params = parse_qs(url[1])
        else:
            self.send_response(300)
            self.send_header("Content-type", "text/html")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes("No params", "utf-8"))
            return

        if url_path == "/user":
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

    def do_PUT(self):
        if self.path.__contains__('?'):
            url = self.path.split('?')
            url_path = url[0]
            url_params = parse_qs(url[1])
        else:
            self.send_response(300)
            self.send_header("Content-type", "text/html")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes("No params", "utf-8"))
            return

        if url_path == "/user":
            if url_params.__contains__('client_id'):
                user = User(url_params)
                user.put_user(self, con)
            else:
                self.send_response(306)
                self.send_header("Content-type", "text/html")
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(bytes("No client_id", "utf-8"))


if __name__ == "__main__":
    server = HTTPServer((hostName, serverPort), Client)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
