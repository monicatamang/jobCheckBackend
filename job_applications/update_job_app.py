from flask import app, request, Response
import traceback
import dbstatements
import json

# Creating a function that updates a job application
def update_job_app():
    # Trying to get the user's job application data
    try:
        login_token = request.json['loginToken']
        job_app_id = int(request.json['jobAppId'])
        company = request.json.get('company')
        job_posting_url = request.json.get('jobPostingUrl')
        job_position = request.json.get('position')
        job_location = request.json.get('location')
        employment_type = request.json.get('employmentType')
        salary_type = request.json.get('salaryType')
        salary_amount = request.json.get('salaryAmount')
        start_date = request.json.get('startDate')
        due_date = request.json.get('dueDate')
        job_app_status = request.json.get('status')
        applied_date = request.json.get('appliedDate')
        notes = request.json.get('notes')
        
        # If the user sends a login token without content, return a server error response
        if(login_token == ''):
            return Response("User is not logged in.", mimetype="text/plain", status=403)
    except ValueError:
        traceback.print_exc()
        return Response("Invalid data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        return Response("Incorrect or missing key.", mimetype="text/plain", status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong. Please try again.", mimetype="text/plain", status=400)

    # Initializing the UPDATE query and an empty list to store the values
    sql = "UPDATE user_session us INNER JOIN job_application ja ON ja.user_id = us.user_id SET"
    data = []

    # The following if statements have the same comments applied to them:
    # If the user sends one piece of information about their job application, add their information to the UPDATE statement as a column and append the column value to the list

    if(company != None and company != ''):
        sql += " ja.company = ?,"
        data.append(company)
    if(job_posting_url != None and job_posting_url != ''):
        sql += " ja.job_posting_url = ?,"
        data.append(job_posting_url)
    if(job_position != None and job_position != ''):
        sql += " ja.job_position = ?,"
        data.append(job_position)
    if(job_location != None and job_location != ''):
        sql += " ja.job_location = ?,"
        data.append(job_location)
    if(employment_type != None and employment_type != ''):
        sql += " ja.employment_type = ?,"
        data.append(employment_type)
    if(salary_type != None and salary_type != ''):
        sql += " ja.salary_type = ?,"
        data.append(salary_type)
    if(salary_amount != None and salary_amount != ''):
        sql += " ja.salary_amount = ?,"
        data.append(salary_amount)
    if(start_date != None and start_date != ''):
        sql += " ja.start_date = ?,"
        data.append(start_date)
    if(due_date != None and due_date != ''):
        sql += " ja.due_date = ?,"
        data.append(due_date)
    if(job_app_status != None and job_app_status != ''):
        sql += " ja.status = ?,"
        data.append(job_app_status)
    if(applied_date != None and applied_date != ''):
        sql += " ja.applied_date = ?,"
        data.append(applied_date)
    if(notes != None and notes != ''):
        sql += " ja.notes = ?,"
        data.append(notes)
    
    # Removing the comma at the end of the UPDATE statment
    sql = sql[:-1]
    # Adding the WHERE clause to the UPDATE statement
    sql += " WHERE us.token = ? AND ja.id = ?"
    # Appending the login token to the list
    data.append(login_token)
    data.append(job_app_id)

    # Checking to see if the user's job application is updated in the database
    row_count = dbstatements.run_update_statement(sql, data)

    # If the user's job application is updated, get the updated job application from the database
    if(row_count == 1):
        updated_job_app_list = dbstatements.run_select_statement("SELECT ja.id, ja.company, ja.job_posting_url, ja.job_position, ja.job_location, ja.employment_type, ja.salary_type, ja.salary_amount, ja.start_date, ja.due_date, ja.status, ja.applied_date, ja.notes FROM user_session us INNER JOIN job_application ja ON ja.user_id = us.user_id WHERE us.token = ? AND ja.id = ?", [login_token, job_app_id])
        # If the updated job application is retrieved from the database, send the updated job application as a dictionary
        if(len(updated_job_app_list) == 1):
            updated_job_app = {
                'jobAppId': updated_job_app_list[0][0],
                'company': updated_job_app_list[0][1],
                'jobPostingUrl': updated_job_app_list[0][2],
                'position': updated_job_app_list[0][3],
                'location': updated_job_app_list[0][4],
                'employmentType': updated_job_app_list[0][5],
                'salaryType': updated_job_app_list[0][6],
                'salaryAmount': updated_job_app_list[0][7],
                'startDate': updated_job_app_list[0][8],
                'dueDate': updated_job_app_list[0][9],
                'status': updated_job_app_list[0][10],
                'appliedDate': updated_job_app_list[0][11],
                'notes': updated_job_app_list[0][12]
            }
            # Converting the job application data into JSON data
            updated_job_app_json = json.dumps(updated_job_app, default=str)
            # Sending a client success response with the JSON data
            return Response(updated_job_app_json, mimetype="application/json", status=200)
        # If the updated job application is not retrieved from the database, send a server error response
        else:
            return Response("Something went wrong. Please refresh the page.", mimetype="text/plain", status=500)
    # If the user's job application is not updated, send a server error response
    else:
        return Response("Failed to update job application.", mimetype="text/plain", status=500)