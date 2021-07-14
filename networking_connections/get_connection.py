from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that gets a user's networking connections
def get_networking_connections():
    # Trying to get the user's id and connection id
    try:
        user_id = int(request.args['userId'])
        connection_id = request.args.get('connectionId')

        # If the user sends a connection id, convert it into an integer
        if(connection_id != None and connection_id != ''):
            connection_id = int(connection_id)
    except ValueError:
        traceback.print_exc()
        return Response("Invalid data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        return Response("Incorrect or missing key.", mimetype="text/plain", status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong. Please try again.", mimetype="text/plain", status=400)

    # If the user does not send a connection id, get all networking connections that belong to the user id
    if(connection_id == None):
        connections = dbstatements.run_select_statement("SELECT nc.user_id, nc.id, ne.id, ne.event_name, nc.name, nc.company, nc.connection_role, nc.email, nc.phone_number, nc.linkedIn, nc.website, nc.other, nc.notes FROM networking_event ne INNER JOIN networking_connection nc ON nc.networking_event_id = ne.id WHERE nc.user_id = ?", [user_id,])
    # If the user does send a connection id, get the networking connection that belongs to the user id and has the connection id
    else:
        connections = dbstatements.run_select_statement("SELECT nc.user_id, nc.id, ne.id, ne.event_name, nc.name, nc.company, nc.connection_role, nc.email, nc.phone_number, nc.linkedIn, nc.website, nc.other, nc.notes FROM networking_event ne INNER JOIN networking_connection nc ON nc.networking_event_id = ne.id WHERE nc.user_id = ? AND nc.id = ?", [user_id, connection_id])

    # If the networking connections are not retrieved from the database, send a server error response
    if(connections == None):
        return Response("Failed to get networking connections.", mimetype="text/plain", status=500)
    # If the networking connections are retrieved from the database, send the networking connections as a list of dictionaries
    else:
        connections_list = []
        for connection in connections:
            each_connection = {
                'user_id': connection[0],
                'connectionId': connection[1],
                'networkingEventId': connection[2],
                'eventName': connection[3],
                'name': connection[4],
                'company': connection[5],
                'role': connection[6],
                'email': connection[7],
                'phoneNumber': connection[8],
                'linkedIn': connection[9],
                'website': connection[10],
                'other': connection[11],
                'notes': connection[12]
            }
            connections_list.append(each_connection)
        # Converting the networking connections into JSON data
        connections_list_json = json.dumps(connections_list, default=str)
        # Sending a client success response with the JSON data
        return Response(connections_list_json, mimetype="application/json", status=200)