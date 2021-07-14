from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that updates a job reference
def update_job_ref():
    # Trying to get the user's job reference data
    try:
        login_token = request.json['loginToken']
        job_ref_id = int(request.json['jobRefId'])
        name = request.json.get('name')
        position = request.json.get('position')
        company_name = request.json.get('companyName')
        company_address = request.json.get('companyAddress')
        postal_code = request.json.get('postalCode')
        city = request.json.get('city')
        province = request.json.get('province')
        email = request.json.get('email')
        phone_number = request.json.get('phoneNumber')
        notes = request.json.get('notes')

        # If the user send a login token without content, return a client error response
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
    sql = "UPDATE user_session us INNER JOIN job_reference jr ON jr.user_id = us.user_id SET"
    data = []

    # The following if statements have the same comments applied to them:
    # If the user sends one piece of information about their job reference, add their information to the UPDATE statement as a column and append the column value to the list

    if(name != None and name != ''):
        sql += " jr.name = ?,"
        data.append(name)
    if(position != None and position != ''):
        sql += " jr.position = ?,"
        data.append(position)
    if(company_name != None and company_name != ''):
        sql += " jr.company_name = ?,"
        data.append(company_name)
    if(company_address != None and company_address != ''):
        sql += " jr.company_address = ?,"
        data.append(company_address)
    if(postal_code != None and postal_code != ''):
        sql += " jr.postal_code = ?,"
        data.append(postal_code)
    if(city != None and city != ''):
        sql += " jr.city = ?,"
        data.append(city)
    if(province != None and province != ''):
        sql += " jr.province = ?,"
        data.append(province)
    if(email != None and email != ''):
        sql += " jr.email = ?,"
        data.append(email)
    if(phone_number != None and phone_number != ''):
        sql += " jr.phone_number = ?,"
        data.append(phone_number)
    if(notes != None and notes != ''):
        sql += " jr.notes = ?,"
        data.append(notes)

    # Removing the comma at the end of the UPDATE statment
    sql = sql[:-1]
    # Adding the WHERE clause to the UPDATE statement
    sql += " WHERE us.token = ? AND jr.id = ?"
    # Appending the login token to the list
    data.append(login_token)
    data.append(job_ref_id)

    # Checking to see if the user's job reference is updated in the database
    row_count = dbstatements.run_update_statement(sql, data)

    # If the user's job reference is updated, get the updated job application from the database
    if(row_count == 1):
        updated_job_ref_list = dbstatements.run_select_statement("SELECT us.user_id, jr.id, jr.reference_name, jr.job_position, jr.company_name, jr.company_address, jr.postal_code, jr.city, jr.province, jr.email, jr.phone_number, jr.notes FROM user_session us INNER JOIN job_reference jr ON jr.user_id = us.user_id WHERE us.token = ? AND jr.id = ?", [login_token, job_ref_id])
        # If the updated job reference is retrieved from the database, send the updated job reference as a dictionary
        if(len(updated_job_ref_list) == 1):
            updated_job_ref = {
                'userId': updated_job_ref_list[0][0],
                'jobRefd': updated_job_ref_list[0][1],
                'name': updated_job_ref_list[0][2],
                'position': updated_job_ref_list[0][3],
                'companyName': updated_job_ref_list[0][4],
                'companyAddress': updated_job_ref_list[0][5],
                'postalCode': updated_job_ref_list[0][6],
                'city': updated_job_ref_list[0][7],
                'province': updated_job_ref_list[0][8],
                'email': updated_job_ref_list[0][9],
                'phoneNumber': updated_job_ref_list[0][10],
                'notes': updated_job_ref_list[0][11],
            }
            # Converting the job reference data into JSON data
            updated_job_ref_json = json.dumps(updated_job_ref, default=str)
            # Sending a client success response with the JSON data
            return Response(updated_job_ref_json, mimetype="application/json", status=200)
        # If the updated job reference is not retrieved from the database, send a server error response
        else:
            return Response("Something went wrong. Please refresh the page.", mimetype="text/plain", status=500)
    # If the user's job reference is not updated, send a server error response
    else:
        return Response("Failed to update job reference.", mimetype="text/plain", status=500)