from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that creates a interviewer
def create_interviewer():
    # Trying to get the user's interviewer's information
    try:
        login_token = request.json['loginToken']
        interview_id = int(request.json['interviewId'])
        job_app_id = int(request.json['jobAppId'])
        name = request.json['interviewerName']
        position = request.json.get('interviewerPosition')
        email = request.json.get('interviewerEmail')
        phone_number = request.json.get('interviewerPhoneNumber')
        other_contact_info = request.json.get('interviewerOtherContactInfo')
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

    # If the user's id is retrieved from the database, create an interviewer
    if(len(user_id_list) == 1):
        interviewer_id = dbstatements.run_insert_statement("INSERT INTO interviewer(user_id, interview_id, job_app_id, name, job_position, email, phone_number, other_contact_info, notes) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", [user_id_list[0][0], interview_id, job_app_id, name, position, email, phone_number, other_contact_info, notes])
        # If a new interviewer id is not created, send a server error response
        if(interviewer_id == None):
            return Response("Failed to create interviewer.", mimetype="text/plain", status=500)
        # If a new interviewer id is created, send the new interviewer as a dictionary
        else:
            interviewer = {
                'userId': user_id_list[0][0],
                'interviewerId': interviewer_id,
                'interviewId': interview_id,
                'jobAppId': job_app_id,
                'interviewerName': name,
                'interviewerPosition': position,
                'interviewerEmail': email,
                'interviewerPhoneNumber': phone_number,
                'interviewerOtherContactInfo': other_contact_info,
                'notes': notes
            }
            # Converting the new interviewer into JSON data
            interviewer_json = json.dumps(interviewer, default=str)
            # Sending a client success response with the JSON data
            return Response(interviewer_json, mimetype="application/json", status=201)
    # If the user's id is not retrieved from the database, send a client error response
    else:
        return Response("User is not logged in.", mimetype="text/plain", status=403)