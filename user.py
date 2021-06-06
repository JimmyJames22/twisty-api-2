import json

import mysql.connector
from flask import Response


class User:
    def __init__(self, params):
        self.client_id = params["client_id"]
        self.firstname = params["firstname"]
        self.lastname = params["lastname"]
        self.email = params["email"]
        self.password = params["password"]
        self.phone = params["phone"]
        if params['addresses'] is None:
            self.addresses = None
        else:
            self.addresses = json.loads(params["addresses"])

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

    def get_user(self):
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            database="users"
        )

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
            json = {'firstname': check_result[0][0], 'lastname': check_result[0][1], 'email': check_result[0][2],
                    'phone': check_result[0][3], 'password': check_result[1][1]}

            addresses = []
            for x in range(2, len(check_result)):
                address = {'description': check_result[x][0], 'address_1': check_result[x][1],
                           'address_2': check_result[x][2], 'city': check_result[x][3], 'state': check_result[x][4],
                           'zipcode': check_result[x][5]}
                addresses.append(address)

            json['addresses'] = addresses

            resp = Response(json.__str__())
            return resp
        else:
            resp_error = {'Method': 'GET', 'Error': 'Invalid client_id'}
            resp = Response(str(resp_error), 404)
            return resp

    def post_user(self):
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            database="users"
        )

        check_cursor = con.cursor()
        check_query = "SELECT clientid FROM userlist WHERE email = %s"
        check_cursor.execute(check_query, [self.email])

        check_result = check_cursor.fetchall()

        if len(check_result) > 0:
            resp_error = {'Method': 'POST', 'Error': 'Email not unique'}
            resp = Response(str(resp_error), 404)
            return resp

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

        json = {'Method': 'POST', 'client_id': self.client_id, 'firstname': self.firstname, 'lastname': self.lastname, 'email': self.email, 'phone': self.phone,
                'password': self.password, 'addresses': self.addresses}

        resp = Response(str(json), 200)
        return resp

    def put_user(self):
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            database="users"
        )

        cursor = con.cursor()

        vals_updated = []
        addresses_added = 0
        addresses_deleted = 0

        id_query = "SELECT firstname FROM userlist WHERE clientid = %s"
        cursor.execute(id_query, [self.client_id])
        id_result = cursor.fetchall()
        if len(id_result) != 1:
            resp_error = {'Method': 'PUT', 'Error': 'Invalid client_id'}
            resp = Response(str(resp_error), 404)
            return resp

        if self.email is not None:
            check_query = "SELECT clientid FROM userlist WHERE email = %s"
            cursor.execute(check_query, [self.email])
            check_result = cursor.fetchall()
            if len(check_result) > 0:
                resp_error = {'Method': 'PUT', 'Error': 'Email not unique'}
                resp = Response(str(resp_error), 404)
                return resp
            query = "UPDATE userlist SET email = %s WHERE clientid = %s"
            cursor.execute(query, [self.email, self.client_id])
            con.commit()
            query = "UPDATE userlogin SET email = %s WHERE clientid = %s"
            cursor.execute(query, [self.email, self.client_id])
            con.commit()
            vals_updated.append('EMAIL')
        if self.firstname is not None:
            query = "UPDATE userlist SET firstname = %s WHERE clientid = %s"
            cursor.execute(query, [self.firstname, self.client_id])
            con.commit()
            vals_updated.append('FIRSTNAME')
        if self.lastname is not None:
            query = "UPDATE userlist SET lastname = %s WHERE clientid = %s"
            cursor.execute(query, [self.lastname, self.client_id])
            con.commit()
            vals_updated.append('LASTNAME')
        if self.password is not None:
            query = "UPDATE userlogin SET password = %s WHERE clientid = %s"
            cursor.execute(query, [self.password, self.client_id])
            con.commit()
            vals_updated.append('PASSWORD')
        if self.phone is not None:
            query = "UPDATE userlist SET phone = %s WHERE clientid = %s"
            cursor.execute(query, [self.phone, self.client_id])
            con.commit()
            vals_updated.append('PHONE')
        for address in self.addresses:
            if address[len(address) - 1] == "ADD":
                address.pop(len(address) - 1)
                address.append(self.client_id)
                query = "INSERT INTO useraddresses (description, streetAddress1, streetAddress2, city, state, zipcode, clientid) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, address)
                con.commit()
                addresses_added += 1
            elif address[len(address) - 1] == "DELETE":
                address.pop(len(address) - 1)
                query = "DELETE FROM useraddresses WHERE description = %s"
                cursor.execute(query, address)
                con.commit()
                addresses_deleted += 1

        resp_string = {'Method': 'PUT', "Values changed": vals_updated, 'Addresses updated': addresses_added,
                       'addresses deleted': addresses_deleted}

        resp = Response(str(resp_string), 200)
        return resp

    def delete_user(self):
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            database="users"
        )

        cursor = con.cursor()

        name_query = "SELECT firstname FROM userlist WHERE clientid = %s"
        cursor.execute(name_query, [self.client_id])
        name_result = cursor.fetchall()

        name_query = "SELECT lastname FROM userlist WHERE clientid = %s"
        cursor.execute(name_query, [self.client_id])
        name_result += cursor.fetchall()

        if len(name_result) == 2:
            firstname = name_result[0][0]
            lastname = name_result[1][0]
        else:
            resp_error = {'Method': 'DELETE', 'Error': 'Invalid client_id'}
            resp = Response(str(resp_error), 404)
            return resp

        userlist_query = "DELETE FROM userlist WHERE clientid = %s"
        cursor.execute(userlist_query, [self.client_id])

        useraddresses_query = "DELETE FROM useraddresses WHERE clientid = %s"
        cursor.execute(useraddresses_query, [self.client_id])

        userhistory_query = "DELETE FROM userhistory WHERE clientid = %s"
        cursor.execute(userhistory_query, [self.client_id])

        userlogin_query = "DELETE FROM userlogin WHERE clientid = %s"
        cursor.execute(userlogin_query, [self.client_id])

        usersettings_query = "DELETE FROM usersettings WHERE clientid = %s"
        cursor.execute(usersettings_query, [self.client_id])

        con.commit()

        resp_string = {'method': 'DELETE', 'firstname': firstname, 'lastname': lastname}
        resp = Response(str(resp_string), 200)
        return resp
