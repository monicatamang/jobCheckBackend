from flask import request, Response
import traceback
import dbstatements

# Creating a function that will delete a user's interview
def delete_interview():
    # Trying to get the user's login token and interview id
    try:
        login_token = request.json['loginToken']
        interview_id = int(request.json['interviewId'])
    
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

    # Checking to see if the interview is deleted
    row_count = dbstatements.run_delete_statement("DELETE i FROM user_session us INNER JOIN interview i WHERE us.token = ? AND i.id = ?", [login_token, interview_id])

    # If the job application is deleted, send a client success response
    if(row_count == 1):
        return Response(status=204)
    # If the job application is not deleted, send a server error response
    else:
        return Response("Failed to delete interview.", mimetype="text/plain", status=500)