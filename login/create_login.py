from flask import request, Response
import traceback
import dbstatements
import json
import user_token
import hashlib
import dbsalt
import email_format

# Creating a function that logs in a user
def login_user():
    # Trying to get the user's email and password
    try:
        email = request.json['email']
        password = request.json['password']

        # If the user sends an email or password without content, return a client error response
        if(email == "" or password == ""):
            return Response("Invalid data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        return Response("Incorrect or missing key.", mimetype="text/plain", status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong.Please try again.", mimetype="text/plain", status=400)

    # Checking to see if the user signed up with a valid email
    is_email_valid = email_format.check_email_format(email)
    # If the user did not send a valid email, send a client error response
    if(is_email_valid == False):
        return Response("Invalid email. Please enter a valid email address.", mimetype="text/plain", status=400)

    # Getting the user's salt from the database given the user's email
    salt = dbsalt.get_salt(email)
    # If the user's salt is not retrieved from the database, send a server error response
    if(salt == None):
        return Response("User is not logged in.", mimetype="text/plain", status=403)
    # If the user's salt is retrieved from the database, salt and hash the user's password
    else:
        password = salt + password
        password = hashlib.sha512(password.encode()).hexdigest()

    # Checking to see if the user's email and password matches with the database records
    db_records = dbstatements.run_select_statement("SELECT id, first_name, last_name, email, password FROM users WHERE email = ? AND password = ?", [email, password])
    
    # If the user's email and password matches, create a login token
    if(len(db_records) == 1):
        token = user_token.create_user_token(db_records[0][0])
        # If a login token is not created, send a server error response
        if(token == None):
            return Response("Failed to log in.", mimetype="text/plain", status=500)
        # If a login token is created, send the user's data with the login token as a dictionary
        else:
            user_data = {
                'userId': db_records[0][0],
                'firstName': db_records[0][1],
                'lastName': db_records[0][2],
                'email': db_records[0][3],
                'loginToken': token
            }
            # Converting the user's data into JSON data
            user_data_json = json.dumps(user_data, default=str)
            # Sending a client success response with the JSON data
            return Response(user_data_json, mimetype="application/json", status=201)
    # If the user's email and password does not match, send a server error response
    else:
        return Response("Failed to log in.", mimetype="text/plain", status=500)