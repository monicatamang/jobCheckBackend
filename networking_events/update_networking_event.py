from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that updates a networking event
def update_networking_event():
    # Trying to get the user's networking event data
    try:
        login_token = request.json['loginToken']
        networking_event_id = int(request.json['networkingEventId'])
        event_name = request.json.get('eventName')
        event_date = request.json.get('eventDate')
        start_time = request.json.get('startTime')
        start_time_period = request.json.get('startTimePeriod')
        end_time = request.json.get('endTime')
        end_time_period = request.json.get('endTimePeriod')
        time_zone = request.json.get('timeZone')
        event_type = request.json.get('eventType')
        event_location = request.json.get('location')
        event_status = request.json.get('status')
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
    sql = "UPDATE user_session us INNER JOIN networking_event ne ON ne.user_id = us.user_id SET"
    data = []

    # The following if statements have the same comments applied to them:
    # If the user sends one piece of information about their networking event, add their information to the UPDATE statement as a column and append the column value to the list

    if(event_name != None and event_name != ''):
        sql += " ne.event_name = ?,"
        data.append(event_name)
    if(event_date != None and event_date != ''):
        sql += " ne.event_date = ?,"
        data.append(event_date)
    if(start_time != None and start_time != ''):
        sql += " ne.start_time = ?,"
        data.append(start_time)
    if(start_time_period != None and start_time_period != ''):
        sql += " ne.start_time_period = ?,"
        data.append(start_time_period)
    if(end_time != None and end_time != ''):
        sql += " ne.end_time = ?,"
        data.append(end_time)
    if(end_time_period != None and end_time_period != ''):
        sql += " ne.end_time_period = ?,"
        data.append(end_time_period)
    if(time_zone != None and time_zone != ''):
        sql += " ne.time_zone = ?,"
        data.append(time_zone)
    if(event_type != None and event_type != ''):
        sql += " ne.event_type = ?,"
        data.append(event_type)
    if(event_location != None and event_location != ''):
        sql += " ne.event_location = ?,"
        data.append(event_location)
    if(event_status != None and event_status != ''):
        sql += " ne.event_status = ?,"
        data.append(event_status)
    if(notes != None and notes != ''):
        sql += " ne.notes = ?,"
        data.append(notes)

    # Removing the comma at the end of the UPDATE statment
    sql = sql[:-1]
    # Adding the WHERE clause to the UPDATE statement
    sql += " WHERE us.token = ? AND ne.id = ?"
    # Appending the login token to the list
    data.append(login_token)
    data.append(networking_event_id)

    # Checking to see if the user's networking event is updated in the database
    row_count = dbstatements.run_update_statement(sql, data)

    # If the networking event is updated, get the updated networking event
    if(row_count == 1):
        updated_networking_event_list = dbstatements.run_select_statement("SELECT us.user_id, ne.id, ne.event_name, ne.event_date, ne.start_time, ne.start_time_period, end_time, end_time_period, ne.time_zone, ne.event_type, ne.event_location, ne.status, ne.notes FROM user_session us INNER JOIN networking_event ne ON ne.user_id = us.user_id WHERE us.token = ? AND ne.id = ?", [login_token, networking_event_id])
        # If the updated networking event is retrieved from the database, send the updated networking event as a dictionary
        if(len(updated_networking_event_list) == 1):
            updated_networking_event = {
                'userId': updated_networking_event_list[0][0],
                'networkingEventId': updated_networking_event_list[0][1],
                'eventName': updated_networking_event_list[0][2],
                'eventDate': updated_networking_event_list[0][3],
                'startTime': updated_networking_event_list[0][4],
                'startTimePeriod': updated_networking_event_list[0][5],
                'endTime': updated_networking_event_list[0][6],
                'endTimePeriod': updated_networking_event_list[0][7],
                'timeZone': updated_networking_event_list[0][8],
                'eventType': updated_networking_event_list[0][9],
                'eventLocation': updated_networking_event_list[0][10],
                'status': updated_networking_event_list[0][11],
                'notes': updated_networking_event_list[0][12]
            }
            # Converting the updated networking event into JSON data
            updated_networking_event_json = json.dumps(updated_networking_event, default=str)
            # Sending a client success response with JSON data
            return Response(updated_networking_event_json, mimetype="application/json", status=200)
        # If the updated networking event is not retrieved from the database, send a server error response
        else:
            return Response("Something went wrong. Please refresh the page.", mimetype="text/plain", status=500)
    # If the networking event is not updated, send a server error response
    else:
        return Response("Failed to update networking event.", mimetype="text/plain", status=500)