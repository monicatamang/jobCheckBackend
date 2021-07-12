from flask import request, Response
import traceback
import dbstatements
import dbsalt
import hashlib

# Creating a function to delete an exisiting user
def delete_user():
    # Trying to get the user's login token and password
    try:
        login_token = request.json['loginToken']
        password = request.json['password']

        # If the user sends a login token or password without content, send a client error response
        if(login_token == "" or password == ""):
            return Response("Invalid data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        return Response("Incorrect or missing key.", mimetype="text/plain", status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong. Please try again.", mimetype="text/plain", status=400)

    # Getting the user's email from the database given the login token
    email_list = dbstatements.run_select_statement("SELECT email FROM users u INNER JOIN user_session us ON us.user_id = u.id WHERE us.token = ?", [login_token,])

    # If the user's email is retrieved from the database, get the user's salt
    if(len(email_list) == 1):
        salt = dbsalt.get_salt(email_list[0][0])
        # If the user's salt is not retrieved from the database, send a server error response
        if(salt == None):
            return Response("An error occurred in the database.", mimetype="text/plain", status=500)
        # If the user's salt is retrieved from the database, salt and hash the user's password
        else:
            password = salt + password
            password = hashlib.sha512(password.encode()).hexdigest()
    # If the user's email is not retrieved from the database, send a server error response
    else:
        return Response("User is not logged in.", mimetype="text/plain", status=511)

    # Checking to see if the user is deleted from the database
    row_count = dbstatements.run_delete_statement("DELETE u FROM users u INNER JOIN user_session us ON us.user_id = u.id WHERE us.token = ?", [login_token, password])
    # If the user is deleted from the database, send a client success response
    if(row_count == 1):
        return Response(status=204)
    # If the user is not deleted from the database, send a client error response
    else:
        return Response("Failed to delete user.", mimetype="text/plain", status=403)