from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that get a user's interviewers
def get_interviewers():
    # Trying to get the user's id and interviewer id
    try:
        user_id = int(request.args['userId'])
        interviewer_id = request.args.get('interviewerId')

        # If the user sends an interviewer id, convert it into an integer
        if(interviewer_id != None and interviewer_id != ''):
            interviewer_id = int(interviewer_id)
    except ValueError:
        traceback.print_exc()
        return Response("Invalid data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        return Response("Incorrect or missing key.", mimetype="text/plain", status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong. Please try again.", mimetype="text/plain", status=400)

    # If the user does not send an interviewer id, get all interviewers that belong to the user id
    if(interviewer_id == None):
        interviewers = dbstatements.run_select_statement("SELECT ja.company, i2.id, i2.interview_id, i2.job_app_id, i2.name, i2.job_position, i2.email, i2.phone_number, i2.other_contact_info, i2.notes FROM job_application ja INNER JOIN interviewer i2 ON i2.job_app_id = ja.id WHERE i2.user_id = ? ORDER BY i2.created_at DESC", [user_id,])
    # If the user does send an interviewer id, get the interviewer that is owned by the user id and has the interviewer id
    else:
        interviewers = dbstatements.run_select_statement("SELECT ja.company, i2.id, i2.interview_id, i2.job_app_id, i2.name, i2.job_position, i2.email, i2.phone_number, i2.other_contact_info, i2.notes FROM job_application ja INNER JOIN interviewer i2 ON i2.job_app_id = ja.id WHERE i2.user_id = ? AND i2.id = ? ORDER BY i2.created_at DESC", [user_id, interviewer_id])

    # If the interviewers are not retrieved from the database, send a server error response
    if(interviewers == None):
        return Response("Failed to get interviewers.", mimetype="text/plain", status=500)
    # If the interviewers are retrieved from the database, send the interviewers as a list of dictionaries
    else:
        interviewers_list = []
        for interviewer in interviewers:
            each_interviewer = {
                'userId': user_id,
                'interviewerId': interviewer[1],
                'interviewId': interviewer[2],
                'jobAppId': interviewer[3],
                'company': interviewer[0],
                'interviewerName': interviewer[4],
                'interviewerPosition': interviewer[5],
                'interviewerEmail': interviewer[6],
                'interviewerPhoneNumber': interviewer[7],
                'interviewerOtherContactInfo': interviewer[8],
                'notes': interviewer[9]
            }
            interviewers_list.append(each_interviewer)
        # Converting the list of interviewers into JSON data
        interviewers_list_json = json.dumps(interviewers_list, default=str)
        # Sending a client success response with the JSON data
        return Response(interviewers_list_json, mimetype="application/json", status=200)