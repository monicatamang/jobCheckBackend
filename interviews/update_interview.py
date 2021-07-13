from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that updates an interview
def update_interview():
    # Trying to get the user's interview information
    try:
        login_token = request.json['loginToken']
        interview_id = int(request.json['interviewId'])
        interview_date = request.json.get('interviewDate')
        interview_time = request.json.get('interviewTime')
        interview_time_period = request.json.get('interviewTimePeriod')
        interview_time_zone = request.json.get('interviewTimeZone')
        interview_type = request.json.get('interviewType')
        interview_location = request.json.get('interviewLocation')
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

    # Initializing the UPDATE query and an empty list to store the values
    sql = "UPDATE user_session us INNER JOIN interview i ON i.user_id = us.user_id SET"
    data = []

    # The following if statements have the same comments applied to them:
    # If the user sends one piece of information about their interview, add their information to the UPDATE statement as a column and append the column value to the list

    if(interview_date != None and interview_date != ''):
        sql += " i.interview_date = ?,"
        data.append(interview_date)
    if(interview_time != None and interview_time != ''):
        sql += " i.interview_time = ?,"
        data.append(interview_time)
    if(interview_time_period != None and interview_time_period != ''):
        sql += " i.interview_time_period = ?,"
        data.append(interview_time_period)
    if(interview_time_zone != None and interview_time_zone != ''):
        sql += " i.interview_time_zone = ?,"
        data.append(interview_time_zone)
    if(interview_type != None and interview_type != ''):
        sql += " i.interview_type = ?,"
        data.append(interview_type)
    if(interview_location != None and interview_location != ''):
        sql += " i.interview_location = ?,"
        data.append(interview_location)
    if(notes != None and notes != ''):
        sql += " i.notes = ?,"
        data.append(notes)

    # Removing the comma at the end of the UPDATE statment
    sql = sql[:-1]
    # Adding the WHERE clause to the UPDATE statement
    sql += " WHERE us.token = ? AND i.id = ?"
    # Appending the login token to the list
    data.append(login_token)
    data.append(interview_id)

    # Checking to see if the user's interview is updated in the database
    row_count = dbstatements.run_update_statement(sql, data)

    # If the user's interview updated in the database, get the updated interview
    if(row_count == 1):
        updated_interview_list = dbstatements.run_select_statement("SELECT ja.id, ja.company, ja.job_position, i.interview_date, i.interview_time, i.interview_time_period, i.interview_time_zone, i.interview_type, i.interview_location, i.notes, i.user_id FROM user_session us INNER JOIN job_application ja ON ja.user_id = us.user_id INNER JOIN interview i ON i.job_app_id = ja.id WHERE us.token = ? AND i.id = ?", [login_token, interview_id])
        # If the updated interview is retrieved from the database, send the updated interview as a dicionary
        if(len(updated_interview_list) == 1):
            updated_interview = {
                'user_id': updated_interview_list[0][10],
                'interviewId': interview_id,
                'jobAppId': updated_interview_list[0][0],
                'company': updated_interview_list[0][1],
                'position': updated_interview_list[0][2],
                'interviewDate': updated_interview_list[0][3],
                'interviewTime': updated_interview_list[0][4],
                'interviewTimePeriod': updated_interview_list[0][5],
                'interviewTimeZone': updated_interview_list[0][6],
                'interviewType': updated_interview_list[0][7],
                'interviewLocation': updated_interview_list[0][8],
                'notes': updated_interview_list[0][9]
            }
            # Converting the updated interview into JSON data
            updated_interview_json = json.dumps(updated_interview, default=str)
            # Sending a client success response with the JSON data
            return Response(updated_interview_json, mimetype="application/json", status=200)
        # If the updated interview is not retrieved from the database, send a server error response
        else:
            return Response("Something went wrong. Please refresh the page.", mimetype="text/plain", status=500)
    # If the user's interview is not updated, send a server error response
    else:
        return Response("Failed to update interview.", mimetype="text/plain", status=500)