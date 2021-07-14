from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that will get a user's interviews
def get_interviews():
    # Trying to get the user's id and interview id
    try:
        user_id = int(request.args['userId'])
        interview_id = request.args.get('interviewId')

        # If the user does send an interview id, convert it into an integer
        if(interview_id != None and interview_id != ''):
            interview_id = int(interview_id)
    except ValueError:
        traceback.print_exc()
        return Response("Invalid data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        return Response("Incorrect or missing key.", mimetype="text/plain", status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong. Please try again.", mimetype="text/plain", status=400)

    # If the user does not send an interview id, get all interviews that belong to the user id
    if(interview_id == None):
        interviews = dbstatements.run_select_statement("SELECT ja.id, ja.company, ja.job_position, i.interview_date, i.interview_time, i.interview_time_period, i.interview_time_zone, i.interview_type, i.interview_location, i.notes, i.id FROM job_application ja INNER JOIN interview i ON i.job_app_id = ja.id WHERE i.user_id = ? ORDER BY i.created_at DESC", [user_id,])
    # If the user does send an interview id, get the interview that belongs the user id and has the interview id
    else:
        interviews = dbstatements.run_select_statement("SELECT ja.id, ja.company, ja.job_position, i.interview_date, i.interview_time, i.interview_time_period, i.interview_time_zone, i.interview_type, i.interview_location, i.notes, i.id FROM job_application ja INNER JOIN interview i ON i.job_app_id = ja.id WHERE i.user_id = ? AND i.id = ? ORDER BY i.created_at DESC", [user_id, interview_id])

    # If the user's interviews are not retrieved from the database, send a server error response
    if(interviews == None):
        return Response("Failed to get interviews.", mimetype="text/plain", status=500)
    # If the user's interviews are retrieved from the database, send the user's interviews as a list of dictionaries
    else:
        interview_list = []
        for interview in interviews:
            each_interview = {
                'userId': user_id,
                'interviewId': interview[10],
                'jobAppId': interview[0],
                'company': interview[1],
                'position': interview[2],
                'interviewDate': interview[3],
                'interviewTime': interview[4],
                'interviewTimePeriod': interview[5],
                'interviewTimeZone': interview[6],
                'interviewType': interview[7],
                'interviewLocation': interview[8],
                'notes': interview[9]
            }
            interview_list.append(each_interview)
        # Converting the interview list into JSON data
        interview_list_json = json.dumps(interview_list, default=str)
        # Sending a client success response with the JSON data
        return Response(interview_list_json, mimetype="application/json", status=200)