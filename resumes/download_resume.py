from flask import request, Response, send_from_directory
from flask.helpers import make_response
import dbstatements
import traceback
import json

# Creating a function that checks to see if the user is allowed to download their resume
def download_resume_file(name):
    # Trying to get the user's login token and resume id
    try:
        login_token = request.headers['Login-Token']
        resume_id = int(request.args['resumeId'])

        # If the user sends a login token without content, send a client error response
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

    # Checking to see if the user's login token and resume id matches with the database records
    db_records = dbstatements.run_select_statement("SELECT us.token, r.id FROM user_session us INNER JOIN resume r ON r.user_id = us.user_id WHERE us.token = ? AND r.id = ?", [login_token, resume_id])

    # If the user's login token and resume id matches with the database records, send the user's resume
    if(len(db_records) == 1):
        # Trying to send the user's resume
        try:
            return send_from_directory("resume_uploads/", name, as_attachment=True)
        except FileNotFoundError:
            traceback.print_exc()
            return Response("File not found.", mimetype="text/plain", status=403)
        except:
            traceback.print_exc()
            return Response("Something went wrong. Please refresh the page.", mimetype="text/plain", status=403)
    # If the user's login token and resume id does not match with the database records, send a client error response
    else:
        return Response("Failed to download resume.", mimetype="text/plain", status=403)

# Creating a function that get's the user's resume file name from the database
def get_resume_name_from_db():
    # Trying to get the user's login token and resume id
    try:
        login_token = request.headers['Login-Token']
        resume_id = int(request.args['resumeId'])

        # If the user sends a login token without content, send a client error response
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

    # Getting the user's resume filename from the database given the login token and resume id
    resume_filename_list = dbstatements.run_select_statement("SELECT r.resume_file FROM user_session us INNER JOIN resume r ON r.user_id = us.user_id WHERE us.token = ? AND r.id = ?", [login_token, resume_id])

    # If the resume filename is retrieved from the database, convert the resume filename into JSON data
    if(len(resume_filename_list) == 1):
        resume_filename_json = json.dumps(resume_filename_list[0][0])
        # Returning a client success response with the JSON data
        return Response(resume_filename_json, mimetype="application/json", status=200)
    # If the resume filename is not retrieved from the database, send a server error response
    else:
        return Response("Failed to retrieve resume.", mimetype="text/plain", status=500)