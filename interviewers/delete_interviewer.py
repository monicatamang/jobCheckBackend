from flask import request, Response
import traceback
import dbstatements

# Creating a function that deletes an interviewer
def delete_interviewer():
    # Trying to get the user's login token and interviewer id
    try:
        login_token = request.json['loginToken']
        interviewer_id = int(request.json['interviewerId'])

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

    # Checking to see if the interviewer is deleted from the database
    row_count = dbstatements.run_delete_statement("DELETE i2 FROM user_session us INNER JOIN interviewer i2 WHERE us.token = ? AND i2.id = ?", [login_token, interviewer_id])

    # If the interviewer is deleted from the database, send a client success response
    if(row_count == 1):
        return Response(status=204)
    # If the interviewer is not deleted from the database, send a server error response
    else:
        return Response("Failed to delete interviewer.", mimetype="text/plain", status=500)