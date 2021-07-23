from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that gets the user's cover letter file data from the database
def get_cover_letter_file():
    # Trying to get the user's login token and job application id
    try:
        login_token = request.headers['Login-Token']
        job_app_id = int(request.args['jobAppId'])

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

    # Getting the user's cover letter file data from the database given the login token and job application id
    cover_letter_file_list = dbstatements.run_select_statement("SELECT cl.user_id, cl.job_app_id, cl.resume_file, cl.created_at FROM user_session us INNER JOIN cover_letter cl ON cl.user_id = us.user_id WHERE us.token = ? AND cl.job_app_id = ?", [login_token, job_app_id])

    # If the resume file data is retrieved from the database, send the data as a dictionary
    if(len(cover_letter_file_list) == 1):
        cover_letter_file = {
            'userId': cover_letter_file_list[0][0],
            'jobAppId': cover_letter_file_list[0][1],
            'coverLetterFile': cover_letter_file_list[0][2],
            'createdAt': cover_letter_file_list[0][3]
        }
        # Converting the cover letter file data into JSON data
        cover_letter_file_json = json.dumps(cover_letter_file, default=str)
        # Sending a client success response with the JSON data
        return Response(cover_letter_file_json, mimetype="application/json", status=200)
    # If the cover letter file data is not retrieved from the database, send a client error response
    else:
        return Response("Failed to get cover letter file.", mimetype="text/plain", status=403)