from flask import request, Response
import traceback
import dbsalt
import dbstatements
import json
import hashlib
import email_format

# Creating a function that updates a user's information
def update_user():
    try:
        login_token = request.json['loginToken']
        first_name = request.json.get('firstName')
        last_name = request.json.get('lastName')
        email = request.json.get('email')
        password = request.json.get('password')
    except KeyError:
        traceback.print_exc()
        return Response("Incorrect or missing key.", mimetype="text/plain", status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong. Please try again.", mimetype="text/plain", status=400)

    # Initializing the UPDATE query and an empty list to store the values    
    sql = "UPDATE users u INNER JOIN user_session us ON u.id = us.user_id SET"
    data = []

    # The following if statements have the same comments applied to them:
    # If the user sends either a first name, last name, email and/or password, add their information to the UPDATE statement as a column and append the column value to the list
    
    if(email != None and email != ''):
        # Checking to see if the user's email address is valid
        is_email_valid = email_format.check_email_format(email)
        # If the format of the user's email address is not vaild, send a server error response
        if(is_email_valid == False):
            return Response("Invalid email. Please enter a valid email address.", mimetype="text/plain", status=400)
        # If the format of the user's email address is vaild, add the email sql statement and value to the UPDATE statement and list
        else:
            sql += " u.email = ?,"
            data.append(email)
    if(first_name != None and first_name != ''):
        sql += " u.first_name = ?,"
        data.append(first_name)
    if(last_name != None and last_name != ''):
        sql += " u.last_name = ?,"
        data.append(last_name)
    if(password != None and password != ''):
        # Creating a new salt 
        salt = dbsalt.create_salt()
        # Salting and hashing the new password
        password = salt + password
        password = hashlib.sha512(password.encode()).hexdigest()
        # Adding the new password and salt sql statement and values to the UPDATE statement and list
        sql += " u.password = ?, u.salt = ?,"
        data.append(password)
        data.append(salt)

    # Removing the comma at the end of the UPDATE statment
    sql = sql[:-1]
    # Adding the WHERE clause to the UPDATE statement
    sql += " WHERE us.token = ?"
    # Appending the login token to the list
    data.append(login_token)

    # Checking to see if the user's information is updated in the database
    row_count = dbstatements.run_update_statement(sql, data)

    # If the user's information is updated, get the updated data from the database
    if(row_count == 1):
        db_updated_records = dbstatements.run_select_statement("SELECT u.id, u.first_name, u.last_name, u.email, us.token FROM users u INNER JOIN user_session us ON us.user_id = u.id WHERE us.token = ?", [login_token,])
        # If the updated data is not retrieved from the database, send a server error response
        if(db_updated_records == None):
            return Response("An error has occurred in the database. Please refresh the page.", mimetype="text/plain", status=500)
        # If the updated data is retrieved from the database, send the updated data as a dictionary
        else:
            updated_data = {
                'userId': db_updated_records[0][0],
                'firstName': db_updated_records[0][1],
                'lastName': db_updated_records[0][2],
                'email': db_updated_records[0][3],
            }
            # Converting the updated data into JSON data
            updated_data_json = json.dumps(updated_data, default=str)
            # Sending a client success resposnse with the JSON data
            return Response(updated_data_json, mimetype="application/json", status=200)
    # If the user's information is not updated, send a server error response
    else:
        return Response("Failed to update user.", mimetype="text/plain", status=500)