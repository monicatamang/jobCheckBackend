from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that creates a new job reference
def create_job_ref():
    # Trying to get the user's job reference data
    try:
        login_token = request.json['loginToken']
        name = request.json['name']
        position = request.json['position']
        company_name = request.json.get('companyName')
        company_address = request.json.get('companyAddress')
        postal_code = request.json.get('postalCode')
        city = request.json['city']
        province = request.json['province']
        email = request.json.get('email')
        phone_number = request.json.get('phoneNumber')
        notes = request.json.get('notes')

        # If the user sends a login token, name, position, city or province without content, send a client error response
        if(login_token == '' or name == '' or position == '' or city == '' or province == ''):
            return Response("Invalid data.", mimetype="text/plain", status=403)
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

    # If the user's id is retrieved from the database, create a new job reference
    if(len(user_id_list) == 1):
        job_ref_id = dbstatements.run_insert_statement("INSERT INTO job_reference(user_id, company_name, reference_name, job_position, company_address, postal_code, city, province, email, phone_number, notes) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [user_id_list[0][0], company_name, name, position, company_address, postal_code, city, province, email, phone_number, notes])
        # If a new job reference id is not created, send a server error response
        if(job_ref_id == None):
            return Response("Failed to create job reference.", mimetype="text/plain", status=500)
        # If a new job reference id is created, send the new job reference as a dictionary
        else:
            job_reference = {
                'userId': user_id_list[0][0],
                'jobRefId': job_ref_id,
                'name': name,
                'position': position,
                'companyName': company_name,
                'companyAddress': company_address,
                'postalCode': postal_code,
                'city': city,
                'province': province,
                'email': email,
                'phoneNumber': phone_number,
                'notes': notes
            }
            # Converting the job reference to JSON data
            job_reference_json = json.dumps(job_reference, default=str)
            # Sending a client success response with the JSON data
            return Response(job_reference_json, mimetype="application/json", status=201)
    # If the user's id is not retrieved from the database, send a client error response
    else:
        return Response("User is not logged in.", mimetype="text/plain", status=403)