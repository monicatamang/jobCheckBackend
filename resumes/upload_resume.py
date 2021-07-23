import os
from flask import request, Response
from werkzeug.utils import secure_filename
import traceback
import dbstatements
import json
import secrets
from app import RESUME_UPLOAD_FOLDER, ALLOWED_EXTENSIONS

# Checking to see if the file is valid
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Creating a function that stores the user's resume into the folder
def store_resume_file():
    # If the user's resume does not have a file extension, send a server error response
    if 'resumeFile' not in request.files:
        return Response("Failed to upload resume.", mimetype="text/plain", status=500)
    file = request.files['resumeFile']
    # If the user does not select a resume file, send a server error response
    if(file.filename == ''):
        return Response("Invalid resume file.", mimetype="text/plain", status=500)
    # If the user sends a resume with a valid extension, secure the file and change the name of the file
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = secrets.token_hex(10) + "_" + filename
        # Saving the user's resume to the folder
        file.save(os.path.join(RESUME_UPLOAD_FOLDER, filename))
        return db_upload_resume(filename)
    
# Creating a function that will upload the user's resume to the database
def db_upload_resume(filename):
    # Trying to get the user's login token and job application id
    try:
        login_token = request.form['loginToken']
        job_app_id = int(request.form['jobAppId'])

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

    # If the user's id is retrieved from the database, store the user's resume into the database
    if(len(user_id_list) == 1):
        resume_id = dbstatements.run_insert_statement("INSERT INTO resume(user_id, job_app_id, resume_file) VALUES(?, ?, ?)", [user_id_list[0][0], job_app_id, filename])
        # If a new resume id is not created, send a server error response
        if(resume_id == None):
            return Response("Failed to upload resume.", mimetype="text/plain", status=500)
        # If a new resume id is created, get the resume creation date from the database
        else:
            resume_created_at_list = dbstatements.run_select_statement("SELECT created_at FROM resume WHERE id = ?", [resume_id,])
            # If the resume creation date is not retrieved from the database, send a server error response
            if(resume_created_at_list == None):
                return Response("Something went wrong. Please refresh the page.", mimetype="text/plain", status=500)
            # If the resume creation date is retrieved from the database, send the user's resume data as a dictionary
            else:
                user_resume_file = {
                    'user_id': user_id_list[0][0],
                    'resumeId': resume_id,
                    'jobAppId': job_app_id,
                    'resumeFile': filename,
                    'createdAt': resume_created_at_list[0][0]
                }
                # Converting the user's resume data into JSON data
                user_resume_file_json = json.dumps(user_resume_file, default=str)
                # Sending a client success response with the JSON data
                return Response(user_resume_file_json, mimetype="application/json", status=201)