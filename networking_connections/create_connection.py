from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that creates a networking connection
def create_networking_connection():
    # Trying to get the user's networking connection data
    try:
        login_token = request.json['loginToken']
        networking_event_id = int(request.json['networkingEventId'])
        name = request.json['name']
        company = request.json.get('company')
        role = request.json.get('role')
        email = request.json.get('email')
        phone_number = request.json.get('phoneNumber')
        linkedIn = request.json.get('linkedIn')
        website = request.json.get('website')
        other = request.json.get('other')
        notes = request.json.get('notes')

        # If the user sends a login token without content, return a client error response
        if(login_token == ''):
            return Response("Invalid login token.", mimetype="text/plain", status=403)
    except ValueError:
        traceback.print_exc()
        return Response("Invalid data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        return Response("Incorrect or missing key.", mimetype="text/plain", status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong. Please try again.", mimetype="text/plain", status=400)

    # Getting the user's id from the database given the login token
    user_id_list = dbstatements.run_select_statement("SELECT user_id FROM user_session WHERE token = ?", [login_token,])

    # If the user's id is retrieved from the database, create a new networking connection
    if(len(user_id_list) == 1):
        connection_id = dbstatements.run_insert_statement("INSERT INTO networking_connection(user_id, networking_event_id, name, company, connection_role, email, phone_number, linkedIn, website, other, notes) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [user_id_list[0][0], networking_event_id, name, company, role, email, phone_number, linkedIn, website, other, notes])
        # If a networking connection id is not created, send a server error response
        if(connection_id == None):
            return Response("Failed to create networking connection.", mimetype="text/plain", status=500)
        # If a networking connection is is created, send the new networking connection as a dictionary
        else:
            networking_connection = {
                'userId': user_id_list[0][0],
                'connectionId': connection_id,
                'networkingEventId': networking_event_id,
                'name': name,
                'company': company,
                'role': role,
                'email': email,
                'phoneNumber': phone_number,
                'linkedIn': linkedIn,
                'website': website,
                'other': other,
                'notes': notes
            }
            # Converting the new networking connnection into JSON data
            networking_connection_json = json.dumps(networking_connection, default=str)
            # Sending a client success response with the JSON data
            return Response(networking_connection_json, mimetype="application/json")
    # If the user's id is not retrieved from the database, send a client error response
    else:
        return Response("User is not logged in.", mimetype="text/plain", status=403)