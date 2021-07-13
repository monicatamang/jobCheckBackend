from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that will update a user's interviewer
def update_interviewer():
    # Trying to get the user's interviewer's information
    try:
        login_token = request.json['loginToken']
        interviewer_id = int(request.json['interviewerId'])
        name = request.json.get('interviewerName')
        position = request.json.get('interviewerPosition')
        email = request.json.get('interviewerEmail')
        phone_number = request.json.get('interviewerPhoneNumber')
        other_contact_info = request.json.get('interviewerOtherContactInfo')
        notes = request.json.get('notes')

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

    # Initializing the UPDATE query and an empty list to store the values
    sql = "UPDATE user_session us INNER JOIN interviewer i2 ON i2.user_id = us.user_id SET"
    data = []

    # The following if statements have the same comments applied to them:
    # If the user sends one piece of information about their interviewer, add their information to the UPDATE statement as a column and append the column value to the list

    if(name != None and name != ''):
        sql += " i2.name = ?,"
        data.append(name)
    if(position != None and position != ''):
        sql += " i2.job_position = ?,"
        data.append(position)
    if(email != None and email != ''):
        sql += " i2.email = ?,"
        data.append(email)
    if(phone_number != None and phone_number != ''):
        sql += " i2.phone_number = ?,"
        data.append(phone_number)
    if(other_contact_info != None and other_contact_info != ''):
        sql += " i2.other_contact_info = ?,"
        data.append(other_contact_info)
    if(notes != None and notes != ''):
        sql += " i2.notes = ?,"
        data.append(notes)

    # Removing the comma at the end of the UPDATE statment
    sql = sql[:-1]
    # Adding the WHERE clause to the UPDATE statement
    sql += " WHERE us.token = ? AND i2.id = ?"
    # Appending the login token to the list
    data.append(login_token)
    data.append(interviewer_id)

    # Checking to see if the user's interviewer is updated in the database
    row_count = dbstatements.run_update_statement(sql, data)

    # If the interviewer is updated, get the updated interviewer from the database
    if(row_count == 1):
        updated_interviewer_list = dbstatements.run_select_statement("SELECT us.user_id, i2.id, i2.interview_id, i2.job_app_id, i2.name, i2.job_position, i2.email, i2.phone_number, i2.other_contact_info, i2.notes FROM user_session us INNER JOIN interviewer i2 ON i2.user_id = i2.user_id WHERE us.token = ? AND i2.id = ?", [login_token, interviewer_id])
        # If the updated interviewer is retrieved from the database, send the updated interviewer as a dictionary
        if(len(updated_interviewer_list) == 1):
            updated_interviewer = {
                'userId': updated_interviewer_list[0][0],
                'interviewerId': updated_interviewer_list[0][1],
                'interviewId': updated_interviewer_list[0][2],
                'jobAppId': updated_interviewer_list[0][3],
                'interviewerName': updated_interviewer_list[0][4],
                'interviewerPosition': updated_interviewer_list[0][5],
                'interviewerEmail': updated_interviewer_list[0][6],
                'interviewerPhoneNumber': updated_interviewer_list[0][7],
                'interviewerOtherContactInfo': updated_interviewer_list[0][8],
                'notes': updated_interviewer_list[0][9]
            }
            # Converting the updated interviewer into JSON data
            updated_interviewer_json = json.dumps(updated_interviewer, default=str)
            # Sending a client success response with the JSON data
            return Response(updated_interviewer_json, mimetype="application/json", status=200)
    # If the interviewer is not updated, send a server error response
    else:
        return Response("Failed to update interviewer.", mimetype="text/plain", status=500)