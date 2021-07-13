from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that gets a user's job appplications
def get_job_app():
    # Trying to get the user's id and job application id
    try:
        user_id = int(request.args['userId'])
        job_app_id = request.args.get('jobAppId')

        # If the user sends a job application id, convert the job application id into an integer
        if(job_app_id != None and job_app_id != ''):
            job_app_id = int(job_app_id)
    except ValueError:
        traceback.print_exc()
        return Response("Invalid data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        return Response("Incorrect or missing key.", mimetype="text/plain", status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong. Please try again.", mimetype="text/plain", status=400)

    # If the user does not send a job application id, get all job applications that are owned by the user id
    if(job_app_id == None):
        job_apps = dbstatements.run_select_statement("SELECT id, company, job_posting_url, job_position, job_location, employment_type, salary_type, salary_amount, start_date, due_date, status, applied_date, notes FROM job_application WHERE user_id = ?", [user_id,])
    # If the user does send a job application id, get all job applications that are owned by the user id and has that job application id
    else:
        job_apps = dbstatements.run_select_statement("SELECT id, company, job_posting_url, job_position, job_location, employment_type, salary_type, salary_amount, start_date, due_date, status, applied_date, notes FROM job_application WHERE user_id = ? AND id = ?", [user_id, job_app_id])

    # If the job applications are not retrieved from the database, send a server error response
    if(job_apps == None):
        return Response("Failed to get job application(s).", mimetype="text/plain", status=500)
    # If the job applications are retrieved from the database, send all job applications as a list of dictionaries
    else:
        job_app_list = []
        for job_app in job_apps:
            each_job_app = {
                'userId': user_id,
                'jobAppId': job_app[0],
                'company': job_app[1],
                'jobPostingUrl': job_app[2],
                'position': job_app[3],
                'location': job_app[4],
                'employmentType': job_app[5],
                'salaryType': job_app[6],
                'salaryAmount': job_app[7],
                'startDate': job_app[8],
                'dueDate': job_app[9],
                'status': job_app[10],
                'appliedDate': job_app[11],
                'notes': job_app[12]
            }
            job_app_list.append(each_job_app)
        # Converting the job applications as JSON data
        job_app_list_json = json.dumps(job_app_list, default=str)
        # Sending a client success response with the JSON data
        return Response(job_app_list_json, mimetype="application/json", status=200)