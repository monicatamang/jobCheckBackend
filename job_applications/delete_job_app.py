from flask import app, request, Response
import traceback
import dbstatements

# Creating a function that will delete a user's job application
def delete_job_app():
    # Trying to get the user's login token and job application id
    try:
        login_token = request.json['loginToken']
        job_app_id = int(request.json['jobAppId'])
    
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

    # Checking to see if the job application is deleted
    row_count = dbstatements.run_delete_statement("DELETE ja FROM user_session us INNER JOIN job_application ja WHERE us.token = ? AND ja.id = ?", [login_token, job_app_id])

    # If the job application is deleted, send a client success response
    if(row_count == 1):
        return Response(status=204)
    # If the job application is not deleted, send a server error response
    else:
        return Response("Failed to delete job application.", mimetype="text/plain", status=500)