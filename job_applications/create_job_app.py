import re
from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that creates a new job application
def create_job_app():
    # Trying to get the user's job application data
    try:
        login_token = request.json['loginToken']
        company = request.json['company']
        job_posting_url = request.json.get('jobPostingUrl')
        job_position = request.json['position']
        job_location = request.json.get('location')
        employment_type = request.json.get('employmentType')
        salary_type = request.json.get('salaryType')
        salary_amount = request.json.get('salaryAmount')
        start_date = request.json.get('startDate')
        due_date = request.json.get('dueDate')
        job_app_status = request.json.get('status')
        applied_date = request.json.get('appliedDate')
        notes = request.json.get('notes')

        # If the user sends a login token, company or job position without content, send a client error response
        if(login_token == '' or company == '' or job_position == ''):
            return Response("Invalid data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        return Response("Incorrect or missing key.", mimetype="text/plain", status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong. Please try again.", mimetype="text/plain", status=400)

    # Getting the user's id from the database given the login token
    user_id_list = dbstatements.run_select_statement("SELECT user_id FROM user_session WHERE token = ?", [login_token,])

    # If the user's id is retrieved from the database, create a new job application
    if(len(user_id_list) == 1):
        # Checking to see if the user's job application is created
        job_app_id = dbstatements.run_insert_statement("INSERT INTO job_application(user_id, company, job_posting_url, job_position, job_location, employment_type, salary_type, salary_amount, start_date, due_date, status, applied_date, notes) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [user_id_list[0][0], company, job_posting_url, job_position, job_location, employment_type, salary_type, salary_amount, start_date, due_date, job_app_status, applied_date, notes])
        # If a new job application id is not created, send a server error response
        if(job_app_id == None):
            return Response("Failed to create a job application.", mimetype="text/plain", status=500)
        # If the a new job application id is created, send the user's job application data
        else:
            new_job_app = {
                'userId': user_id_list[0][0],
                'jobAppId': job_app_id,
                'company': company,
                'jobPostingUrl': job_posting_url,
                'position': job_position,
                'location': job_location,
                'employmentType': employment_type,
                'salaryType': salary_type,
                'salaryAmount': salary_amount,
                'startDate': start_date,
                'dueDate': due_date,
                'status': job_app_status,
                'appliedDate': applied_date,
                'notes': notes
            }
            # Converting the user's job application data into JSON data
            new_job_app_json = json.dumps(new_job_app, default=str)
            # Sending a client success response with the JSON data
            return Response(new_job_app_json, mimetype="application/json", status=201)
    # If the user's id is not retrieved from the database, send a client error response
    else:
        return Response("User is not logged in.", mimetype="text/plain", status=403)