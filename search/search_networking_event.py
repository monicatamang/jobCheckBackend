from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that will return the user's networking event based on the networking event's name
def search_networking_event():
    # Trying to get the user's id and search input
    try:
        user_id = int(request.args['userId'])
        search_input = request.args['searchInput']

        # If the user sends their id and search input without content, send a client error response
        if(search_input == ''):
            return Response("Please enter a valid search input.", mimetype="text/plain", status=403)
    except ValueError:
        traceback.print_exc()
        return Response("Invalid data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        return Response("Incorrect or missing key.", mimetype="text/plain", status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong. Please try again.", mimetype="text/plain", status=400)

    # If the user does not send any data, return a client error response
    if(search_input == None):
        return Response("Please enter a valid search input.", mimetype="text/plain", status=400)
    # If the user does send data, try to find all the user's networking events that matches or closely matches with their search input
    else:
        results = dbstatements.run_select_statement("SELECT id, event_name, event_date, start_time, start_time_period, end_time, end_time_period, time_zone, event_type, event_location, status, notes FROM networking_event WHERE user_id = ? AND event_name LIKE CONCAT('%', ?, '%') ORDER BY created_at DESC", [user_id, search_input])

    # If a database error occurs, send a server error response
    if(results == None):
        return Response(f"Failed to find '{search_input}'.", mimetype="text/plain", status=500)
    # If a match is found, send all matches as a list of dictionaries
    # If no matches are found, an empty list will be returned
    else:
        search_results = []
        for result in results:
            each_result = {
                'userId': user_id,
                'networkingEventId': result[0],
                'eventName': result[1],
                'eventDate': result[2],
                'startTime': result[3],
                'startTimePeriod': result[4],
                'endTime': result[5],
                'endTimePeriod': result[5],
                'timeZone': result[6],
                'eventType': result[7],
                'eventLocation': result[8],
                'status': result[9],
                'notes': result[10]
            }
            search_results.append(each_result)
        # Convert data into JSON
        search_results_json = json.dumps(search_results, default=str)
        # Send a client success response with the JSON data
        return Response(search_results_json, mimetype="application/json", status=200)