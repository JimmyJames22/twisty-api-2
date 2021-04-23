import json


class User:
    def __init__(self, url_params):
        if url_params.__contains__("client_id"):
            self.client_id = url_params["client_id"][0]
        if url_params.__contains__("firstname"):
            self.firstname = url_params["firstname"][0]
        if url_params.__contains__("lastname"):
            self.lastname = url_params["lastname"][0]
        if url_params.__contains__("email"):
            self.email = url_params["email"][0]
        if url_params.__contains__("password"):
            self.password = url_params["password"][0]
        if url_params.__contains__("phone"):
            self.phone = url_params["phone"][0]
        if url_params.__contains__("addresses"):
            self.addresses = json.loads(url_params["addresses"][0])

    def print_user(self):
        try:
            print("client_id: ", self.client_id)
        except AttributeError:
            pass

        try:
            print("firstname: ", self.firstname)
        except AttributeError:
            pass

        try:
            print("lastname: ", self.lastname)
        except AttributeError:
            pass

        try:
            print("email: ", self.email)
        except AttributeError:
            pass

        try:
            print("password: ", self.password)
        except AttributeError:
            pass

        try:
            print("phone: ", self.phone)
        except AttributeError:
            pass

        try:
            print("addreses: ", self.addresses)
        except AttributeError:
            pass

    def get_user(self, client, con):
        check_cursor = con.cursor()
        check_query = "SELECT * FROM userlist WHERE clientid = %s"
        check_cursor.execute(check_query, [self.client_id])
        check_result = check_cursor.fetchall()

        check_query = "SELECT * FROM userlogin WHERE clientid = %s"
        check_cursor.execute(check_query, [self.client_id])
        check_result += check_cursor.fetchall()

        check_query = "SELECT * FROM useraddresses WHERE clientid = %s"
        check_cursor.execute(check_query, [self.client_id])
        check_result += check_cursor.fetchall()

        if len(check_result) > 0:
            client.send_response(200)
            client.send_header("Content-type", "text/html")
            client.send_header('Access-Control-Allow-Origin', '*')
            client.end_headers()
            client.wfile.write(bytes("<h2>User found</h2>", "utf-8"))
            client.wfile.write(bytes("<h3>firstname: %s </h3>" % check_result[0][0], "utf-8"))
            client.wfile.write(bytes("<h3>lastname: %s </h3>" % check_result[0][1], "utf-8"))
            client.wfile.write(bytes("<h3>email: %s </h3>" % check_result[0][2], "utf-8"))
            client.wfile.write(bytes("<h3>phone: %s </h3>" % check_result[0][3], "utf-8"))
            client.wfile.write(bytes("<h3>password: %s </h3>" % check_result[1][1], "utf-8"))
            for x in range(2, len(check_result)):
                client.wfile.write(bytes("<h3>Address %s: %s </h3>" % (str(x-1), check_result[x][0]), "utf-8"))
                client.wfile.write(bytes("<h5>address1: %s </h5>" % check_result[x][1], "utf-8"))
                client.wfile.write(bytes("<h5>address2: %s </h5>" % check_result[x][2], "utf-8"))
                client.wfile.write(bytes("<h5>city: %s </h5>" % check_result[x][3], "utf-8"))
                client.wfile.write(bytes("<h5>state: %s </h5>" % check_result[x][4], "utf-8"))
                client.wfile.write(bytes("<h5>zipcode: %s </h5>" % check_result[x][5], "utf-8"))

        else:
            client.send_response(400)
            client.send_header("Content-type", "text/html")
            client.send_header('Access-Control-Allow-Origin', '*')
            client.end_headers()
            client.wfile.write(bytes("No user found", "utf-8"))

    def post_user(self, client, con):
        check_cursor = con.cursor()
        check_query = "SELECT clientid FROM userlist WHERE email = %s"
        check_cursor.execute(check_query, [self.email])

        check_result = check_cursor.fetchall()

        if len(check_result) > 0:
            client.send_response(299)
            client.send_header("Content-type", "text/html")
            client.send_header('Access-Control-Allow-Origin', '*')
            client.end_headers()
            client.wfile.write(bytes("Email not unique", "utf-8"))
            return

        user_cursor = con.cursor()
        user_list = "INSERT INTO userlist (firstname, lastname, email, phone) VALUES (%s, %s, %s, %s)"
        user_list_val = [self.firstname, self.lastname, self.email, self.phone]
        user_cursor.execute(user_list, user_list_val)

        con.commit()
        self.client_id = user_cursor.lastrowid
        user_cursor2 = con.cursor()

        for address in self.addresses:
            address.append(self.client_id)
            user_addresses = "INSERT INTO useraddresses (description, streetAddress1, streetAddress2, city, state, zipcode, clientid) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            user_cursor2.execute(user_addresses, address)

        user_login = "INSERT INTO userlogin (email, password, clientid) VALUES (%s, %s, %s)"
        user_login_vals = [self.email, self.password, self.client_id]
        user_cursor2.execute(user_login, user_login_vals)

        con.commit()

        client.send_response(200)
        client.send_header("Content-type", "text/html")
        client.send_header('Access-Control-Allow-Origin', '*')
        client.end_headers()
        client.wfile.write(bytes("User created!", "utf-8"))

    def put_user(self, client, con):
        cursor = con.cursor()

        if hasattr(self, 'firstname'):
            query = "UPDATE userlist SET firstname = %s WHERE clientid = %s"
            cursor.execute(query, [self.firstname, self.client_id])
            con.commit()
            print(cursor.rowcount, "record(s) affected FIRSTNAME")

        if hasattr(self, 'lastname'):
            query = "UPDATE userlist SET lastname = %s WHERE clientid = %s"
            cursor.execute(query, [self.lastname, self.client_id])
            con.commit()
            print(cursor.rowcount, "record(s) affected LASTNAME")

        if hasattr(self, 'email'):
            query = "UPDATE userlist SET email = %s WHERE clientid =                   %s"
            cursor.execute(query, [self.email, self.client_id])
            con.commit()
            print(cursor.rowcount, "record(s) affected EMAIL1")
            query = "UPDATE userlogin SET email = %s WHERE clientid = %s"
            cursor.execute(query, [self.email, self.client_id])
            con.commit()
            print(cursor.rowcount, "record(s) affected EMAIL2")

        if hasattr(self, 'password'):
            query = "UPDATE userlogin SET password = %s WHERE clientid = %s"
            cursor.execute(query, [self.password, self.client_id])
            con.commit()
            print(cursor.rowcount, "record(s) affected PASSWORD")

        if hasattr(self, 'phone'):
            query = "UPDATE userlist SET phone = %s WHERE clientid = %s"
            cursor.execute(query, [self.phone, self.client_id])
            con.commit()
            print(cursor.rowcount, "record(s) affected PHONE")

        for address in self.addresses:
            if address[len(address)-1] == "ADD":
                address.pop(len(address)-1)
                address.append(self.client_id)
                query = "INSERT INTO useraddresses (description, streetAddress1, streetAddress2, city, state, zipcode, clientid) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, address)
                con.commit()
                print("ADDRESS INSERTED")
            elif address[len(address)-1] == "DELETE":
                address.pop(len(address)-1)
                query = "DELETE FROM useraddresses WHERE description = %s"
                cursor.execute(query, address)
                con.commit()
                print("ADDRESS DELETED")
        client.send_response(200)
        client.send_header("Content-type", "text/html")
        client.send_header('Access-Control-Allow-Origin', '*')
        client.end_headers()
        client.wfile.write(bytes("Values updated", "utf-8"))

