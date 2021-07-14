from flask import request, Response
import traceback
import dbstatements

# Creating a function that deletes a job reference
def delete_job_ref():
    # Trying to get the user's login token and job reference id
    try:
        login_token = request.json['loginToken']
        job_ref_id = int(request.json['jobRefId'])

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

    # Checking to see if the user's job reference is deleted from the database
    row_count = dbstatements.run_delete_statement("DELETE jr FROM user_session us INNER JOIN job_reference jr ON jr.user_id = us.user_id WHERE us.token = ? AND jr.id = ?", [login_token, job_ref_id])

    # If the job reference is deleted, send a client success response
    if(row_count == 1):
        return Response(status=204)
    # If the job reference is not deleted, send a server error response
    else:
        return Response("Failed to delete job reference.", mimetype="text/plain", status=500)