from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that creates a networking event
def create_networking_event():
    # Trying to get the user's networking event data
    try:
        login_token = request.json['loginToken']
        event_name = request.json['eventName']
        event_date = request.json['eventDate']
        start_time = request.json['startTime']
        start_time_period = request.json['startTimePeriod']
        end_time = request.json.get('endTime')
        end_time_period = request.json.get('endTimePeriod')
        time_zone = request.json['timeZone']
        event_type = request.json.get('eventType')
        event_location = request.json.get('eventLocation')
        event_status = request.json['eventStatus']
        notes = request.json.get('notes')

        # If the user sends the required data without content, send a client error response
        if(login_token == '' or event_name == '' or event_date == '' or start_time == '' or start_time_period == '' or time_zone == '' or event_status == ''):
            return Response("Invalid data.", mimetype="text/plain", status=403)
    except KeyError:
        traceback.print_exc()
        return Response("Incorrect or missing key.", mimetype="text/plain", status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong. Please try again.", mimetype="text/plain", status=400)

    # Getting the user's id from the database given the login token
    user_id_list = dbstatements.run_select_statement("SELECT user_id FROM user_session WHERE token = ?", [login_token,])

    # If the user's id is retrieved from the database, create a new networking event
    if(len(user_id_list) == 1):
        networking_event_id = dbstatements.run_insert_statement("INSERT INTO networking_event(user_id, status, event_name, event_date, start_time, start_time_period, end_time, end_time_period, time_zone, event_type, event_location, notes) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [user_id_list[0][0], event_status, event_name, event_date, start_time, start_time_period, end_time, end_time_period, time_zone, event_type, event_location, notes])
        # If a new networking event id is not created, send a server error response
        if(networking_event_id == None):
            return Response("Failed to create networking event.", mimetype="text/plain", status=500)
        # If a new networking event id is created, send the new networking event as a dictionary
        else:
            networking_event = {
                'userId': user_id_list[0][0],
                'networkingEventId': networking_event_id,
                'eventName': event_name,
                'eventDate': event_date,
                'startTime': start_time,
                'startTimePeriod': start_time_period,
                'endTime': end_time,
                'endTimePeriod': end_time_period,
                'timeZone': time_zone,
                'eventType': event_type,
                'eventLocation': event_location,
                'eventStatus': event_status,
                'notes': notes
            }
            # Converting the new networking event into JSON data
            networking_event_json = json.dumps(networking_event, default=str)
            # Sending a client success response with the JSON data
            return Response(networking_event_json, mimetype="application/json", status=201)
    # If the user's id is not retrieved from the database, send a client error response
    else:
        return Response("User is not logged in.", mimetype="text/plain", status=403)