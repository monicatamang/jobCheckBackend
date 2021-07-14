from flask import request, Response
import traceback
import dbstatements

# Creating a function that deletes a networking event
def delete_networking_event():
    # Trying to get the user's id and networking id
    try:
        login_token = request.json['loginToken']
        networking_event_id = int(request.json['networkingEventId'])

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

    # Checking to see if the networking event is deleted
    row_count = dbstatements.run_delete_statement("DELETE ne FROM user_session us INNER JOIN networking_event ne ON ne.user_id = us.user_id WHERE us.token = ? AND ne.id = ?", [login_token, networking_event_id])

    # If the networking event is deleted from the database, send a client success response
    if(row_count == 1):
        return Response(status=204)
    # If the networking event is not deleted from the database, send a server error response
    else:
        return Response("Failed to delete networking event.", mimetype="text/plain", status=500)