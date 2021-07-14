from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that gets a user's job references
def get_job_ref():
    # Trying to get the user's id and job reference id
    try:
        user_id = int(request.args['userId'])
        job_ref_id = request.args.get('jobRefId')

        # If the user sends a job reference id, convert it into an integer
        if(job_ref_id != None and job_ref_id != ''):
            job_ref_id = int(job_ref_id)
    except ValueError:
        traceback.print_exc()
        return Response("Invalid data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        return Response("Incorrect or missing key.", mimetype="text/plain", status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong. Please try again.", mimetype="text/plain", status=400)

    # If the user does not send a job reference id, get all job references that belong to the user id
    if(job_ref_id == None):
        job_refs = dbstatements.run_select_statement("SELECT id, reference_name, job_position, company_name, company_address, postal_code, city, province, email, phone_number, notes FROM job_reference WHERE user_id = ? ORDER BY created_at DESC", [user_id,])
    # If the user does send a job reference id, get the job reference that belongs to the user id and has the job reference id
    else:
        job_refs = dbstatements.run_select_statement("SELECT id, reference_name, job_position, company_name, company_address, postal_code, city, province, email, phone_number, notes FROM job_reference WHERE user_id = ? AND id = ? ORDER BY created_at DESC", [user_id, job_ref_id])

    # If the job references are not retrieved from the database, send a server error response
    if(job_refs == None):
        return Response("Failed to get job references.", mimetype="text/plain", status=500)
    # If the job references are retrieved from the database, send the user's job references as a list of dictionaries
    else:
        job_refs_list = []
        for job_ref in job_refs:
            each_job_ref = {
                'user_id': user_id,
                'jobRefId': job_ref[0],
                'name': job_ref[1],
                'position': job_ref[2],
                'companyName': job_ref[3],
                'companyAddress': job_ref[4],
                'postalCOde': job_ref[5],
                'city': job_ref[6],
                'province': job_ref[7],
                'email': job_ref[8],
                'phoneNumber': job_ref[9],
                'notes': job_ref[10],
            }
            job_refs_list.append(each_job_ref)
        # Converting the job references into JSON data
        job_refs_list_json = json.dumps(job_refs_list, default=str)
        # Sending a client success response with the JSON data
        return Response(job_refs_list_json, mimetype="application/json", status=200)