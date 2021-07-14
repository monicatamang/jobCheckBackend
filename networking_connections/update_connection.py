from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that updates a networking connection
def update_networking_connection():
    # Trying to get the user's networking connection data
    try:
        login_token = request.json['loginToken']
        connection_id = int(request.json['connectionId'])
        name = request.json.get('name')
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

    # Initializing the UPDATE query and an empty list to store the values
    sql = "UPDATE user_session us INNER JOIN networking_connection nc ON nc.user_id = us.user_id SET"
    data = []

    # The following if statements have the same comments applied to them:
    # If the user sends one piece of information about their networking connection, add their information to the UPDATE statement as a column and append the column value to the list

    if(name != None and name != ''):
        sql += " nc.name = ?,"
        data.append(name)
    if(company != None and company != ''):
        sql += " nc.company = ?,"
        data.append(company)
    if(role != None and role != ''):
        sql += " nc.connection_role = ?,"
        data.append(role)
    if(email != None and email != ''):
        sql += " nc.email = ?,"
        data.append(email)
    if(phone_number != None and phone_number != ''):
        sql += " nc.phone_number = ?,"
        data.append(phone_number)
    if(linkedIn != None and linkedIn != ''):
        sql += " nc.linkedIn = ?,"
        data.append(linkedIn)
    if(website != None and website != ''):
        sql += " nc.website = ?,"
        data.append(website)
    if(other != None and other != ''):
        sql += " nc.other = ?,"
        data.append(other)
    if(notes != None and notes != ''):
        sql += " nc.notes = ?,"
        data.append(notes)

    # Removing the comma at the end of the UPDATE statment
    sql = sql[:-1]
    # Adding the WHERE clause to the UPDATE statement
    sql += " WHERE us.token = ? AND nc.id = ?"
    # Appending the login token to the list
    data.append(login_token)
    data.append(connection_id)

    # Checking to see if the user's networking connection is updated in the database
    row_count = dbstatements.run_update_statement(sql, data)

    # If the networking connection is updated, get the updated networking connection from the database
    if(row_count == 1):
        updated_connection_list = dbstatements.run_select_statement("SELECT nc.user_id, nc.id, nc.networking_event_id, nc.name, nc.company, nc.connection_role, nc.email, nc.phone_number, nc.linkedIn, nc.website, nc.other, nc.notes FROM user_session us INNER JOIN networking_connection nc ON nc.user_id = us.user_id WHERE us.token = ? AND nc.id = ?", [login_token, connection_id])
        # If the updated networking connection is retrieved from the database, send the updated networking connection as a dictionary
        if(len(updated_connection_list) == 1):
            updated_connection = {
                'user_id': updated_connection_list[0][0],
                'connectionId': updated_connection_list[0][1],
                'networkingEventId': updated_connection_list[0][2],
                'name': updated_connection_list[0][3],
                'company': updated_connection_list[0][4],
                'role': updated_connection_list[0][5],
                'email': updated_connection_list[0][6],
                'phoneNumber': updated_connection_list[0][7],
                'linkedIn': updated_connection_list[0][8],
                'website': updated_connection_list[0][9],
                'other': updated_connection_list[0][10],
                'notes': updated_connection_list[0][11] 
            }
            # Converting the updated networking connection into JSON data
            updated_connection_json = json.dumps(updated_connection, default=str)
            # Sending a client success response with the JSON data
            return Response(updated_connection_json, mimetype="application/json", status=200)
        # If the updated networking connection is not retrieved from the database, send a server error response
        else:
            return Response("Something went wrong. Please refresh the page.", mimetype="text/plain", status=500)
    # If the networking connection is not updated, send a server error response
    else:
        return Response("Failed to update networking connection.", mimetype="text/plain", status=500)
