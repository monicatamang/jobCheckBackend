import os
from flask import request, Response
from werkzeug.utils import secure_filename
import traceback
import dbstatements
import json
import secrets

# Initializing a folder to store all users' resumes and setting a limit on the types of text files users can send
UPLOAD_FOLDER = 'cover_letter_uploads/'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pages', 'txt'}

# Checking to see if the file is valid
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Creating a function that stores the user's cover letter into the folder
def store_cover_letter_file():
    # If the user's cover letter does not have a file extension, send a server error response
    if 'coverLetterFile' not in request.files:
        return Response("Failed to upload resume.", mimetype="text/plain", status=500)
    file = request.files['coverLetterFile']
    # If the user does not select a cover letter file, send a server error response
    if(file.filename == ''):
        return Response("Invalid resume file.", mimetype="text/plain", status=500)
    # If the user sends a cover letter with a valid extension, secure the file and change the name of the file
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = secrets.token_hex(10) + "_" + filename
        # Saving the user's cover letter to the folder
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return db_upload_cover_letter(filename)
    
# Creating a function that will upload the user's cover letter to the database
def db_upload_cover_letter(filename):
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

    # If the user's id is retrieved from the database, store the user's cover letter into the database
    if(len(user_id_list) == 1):
        cover_letter_id = dbstatements.run_insert_statement("INSERT INTO cover_letter(user_id, job_app_id, cover_letter_file) VALUES(?, ?, ?)", [user_id_list[0][0], job_app_id, filename])
        # If a new cover letter id is not created, send a server error response
        if(cover_letter_id == None):
            return Response("Failed to upload resume.", mimetype="text/plain", status=500)
        # If a new cover letter id is created, get the cover letter creation date from the database
        else:
            cv_created_At = dbstatements.run_select_statement("SELECT created_at FROM resume WHERE id = ?", [cover_letter_id,])
            # If the cover letter creation date is not retrieved from the database, send a server error response
            if(cv_created_At == None):
                return Response("Something went wrong. Please refresh the page.", mimetype="text/plain", status=500)
            # If the cover letter creation date is retrieved from the database, send the user's cover letter data as a dictionary
            else:
                user_resume_file = {
                    'user_id': user_id_list[0][0],
                    'coverLetterId': cover_letter_id,
                    'jobAppId': job_app_id,
                    'resumeFile': filename,
                    'createdAt': cv_created_At
                }
                # Converting the user's cover letter data into JSON data
                user_resume_file_json = json.dumps(user_resume_file, default=str)
                # Sending a client success response with the JSON data
                return Response(user_resume_file_json, mimetype="application/json", status=201)