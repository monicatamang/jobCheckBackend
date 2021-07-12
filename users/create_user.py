from flask import request, Response
import traceback
import dbstatements
import json
import user_token
import hashlib
import dbsalt
import email_format

# Creating a function that will sign up a user
def signup_user():
    # Trying to get the user's data
    try:
        first_name = request.json['firstName']
        last_name = request.json['lastName']
        email = request.json['email']
        password = request.json['password']
        
        # If the user sends back data without content, send a client error response
        if(first_name == "" or last_name == "" or email == "" or password == ""):
            return Response("Invalid data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        return Response("Incorrect or missing key.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong. Please try again.", mimetype="text/plain", status=400)

    # Checking to see if the user signed up with a valid email
    is_email_valid = email_format.check_email_format(email)
    # If the user did not send a valid email, send a client error response
    if(is_email_valid == False):
        return Response("Invalid email. Please enter a valid email address.", mimetype="text/plain", status=400)

    # Salting and hashing the user's password
    salt = dbsalt.create_salt()
    password = salt + password
    password = hashlib.sha512(password.encode()).hexdigest()

    # Storing the user's data into the database and getting the user's new id
    user_id = dbstatements.run_insert_statement("INSERT INTO users(first_name, last_name, email, password, salt) VALUES(?, ?, ?, ?, ?)", [first_name, last_name, email, password, salt])

    # If a new id is not created, send a server error response
    if(user_id == None):
        return Response("Failed to create a user.", mimetype="text/plain", status=500)
    # If a new id is created, get the user's login token
    else:
        token = user_token.get_user_token(user_id)
        # If a login token is not created, send a server error response
        if(token == None):
            return Response("Failed to log in user.", mimetype="text/plain", status=500)
        # If a login token is created, send the user's data as a dictionary
        else:
            user_data = {
                'userId': user_id,
                'firstName': first_name,
                'lastName': last_name,
                'email': email,
                'loginToken': token
            }
            # Converting the user's data into JSON data
            user_data_json = json.dumps(user_data, default=str)
            # Send a client success response with the JSON data
            return Response(user_data_json, mimetype="application/json", status=201)