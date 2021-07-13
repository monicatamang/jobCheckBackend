from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that creates a new interview
def create_interview():
    # Trying to get the user's interview information
    try:
        login_token = request.json['loginToken']
        job_app_id = int(request.json['jobAppId'])
        interview_date = request.json['date']
        interview_time = request.json['time']
        interview_time_period = request.json['timePeriod']
        interview_time_zone = request.json['timeZone']
        interview_type = request.json.get('type')
        interview_location = request.json.get('location')
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

    # If the user's id is retrieved from the database, create a new interview
    if(len(user_id_list) == 1):
        interview_id = dbstatements.run_insert_statement("INSERT INTO interview(user_id, job_app_id, interview_date, interview_time, interview_time_period, interview_time_zone, interview_type, interview_location, notes) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", [user_id_list[0][0], job_app_id, interview_date, interview_time, interview_time_period, interview_time_zone, interview_type, interview_location, notes])
        # If a new interview id is not created, send a server error response
        if(interview_id == None):
            return Response("Failed to create an interview.", mimetype="text/plain", status=500)
        # If a new interview id is created, send the new interview as a dictionary
        else:
            new_interview = {
                'interviewId': interview_id,
                'jobAppId': job_app_id,
                'date': interview_date,
                'time': interview_time,
                'timePeriod': interview_time_period,
                'timeZone': interview_time_zone,
                'type': interview_type,
                'location': interview_location,
                'notes': notes
            }
            # Converting the new interview into JSON data
            new_interview_json = json.dumps(new_interview, default=str)
            # Sending a client success response with the JSON data
            return Response(new_interview_json, mimetype="application/json", status=201)
    # If the user's id is not retrieved from the database, send a client error response
    else:
        return Response("User is not logged in.", mimetype="text/plain", status=403)