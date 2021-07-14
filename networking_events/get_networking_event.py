from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that get a user's networking events
def get_networking_events():
    # Trying to get the user's id and networking event id
    try:
        user_id = int(request.args['userId'])
        networking_event_id = request.args.get('networkingEventId')

        # If the user sends a networking event id, convert it into an integer
        if(networking_event_id != None and networking_event_id != ''):
            networking_event_id = int(networking_event_id)
    except ValueError:
        traceback.print_exc()
        return Response("Invalid data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        return Response("Incorrect or missing key.", mimetype="text/plain", status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong. Please try again.", mimetype="text/plain", status=400)

    # If the user does not send a networking event id, get all networking events that belong to the user id
    if(networking_event_id == None):
        networking_events = dbstatements.run_select_statement("SELECT id, event_name, event_date, start_time, start_time_period, end_time, end_time_period, time_zone, event_type, event_location, status, notes FROM networking_event WHERE user_id = ?", [user_id,])
    # If the user does send a networking event id, get the networking event that belongs to the user id and has the networking event id
    else:
        networking_events = dbstatements.run_select_statement("SELECT id, event_name, event_date, start_time, start_time_period, end_time, end_time_period, time_zone, event_type, event_location, status, notes FROM networking_event WHERE user_id = ? AND id = ?", [user_id, networking_event_id])

    # If the networking events are not retrieved from the database, send a server error response
    if(networking_events == None):
        return Response("Failed to get networking events.", mimetype="text/plain", status=500)
    # If the networking events are retrieved from the database, send the networking events as a list of dictionaries
    else:
        networking_events_list = []
        for networking_event in networking_events:
            each_networking_event = {
                'userId': user_id,
                'networkingEventId': networking_event[0],
                'eventName': networking_event[1],
                'eventDate': networking_event[2],
                'startTime': networking_event[3],
                'startTimePeriod': networking_event[4],
                'endTime': networking_event[5],
                'endTimePeriod': networking_event[5],
                'timeZone': networking_event[6],
                'eventType': networking_event[7],
                'eventLocation': networking_event[8],
                'status': networking_event[9],
                'notes': networking_event[10],
            }
            networking_events_list.append(each_networking_event)
        # Converting the networking events into JSON data
        networking_events_list_json = json.dumps(networking_events_list, default=str)
        # Sending a client success response with the JSON data
        return Response(networking_events_list_json, mimetype="application/json", status=200)