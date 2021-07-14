from flask import request, Response
import traceback
import dbstatements

# Creating a function that deletes a networking connection
def delete_networking_connection():
    # Trying to get the user's login tokena and connection id
    try:
        login_token = request.json['loginToken']
        connectionId = int(request.json['connectionId'])

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
    
    # Checking to see if the networking connection is deleted from the database
    row_count = dbstatements.run_delete_statement("DELETE nc FROM user_session us INNER JOIN networking_connection nc WHERE us.token = ? AND nc.id = ?", [login_token, connectionId])

    # If the networking connection is deleted from the database, send a client success response
    if(row_count == 1):
        return Response(status=204)
    # If the networking connection is not deleted from the database, send a server error response
    else:
        return Response("Failed to delete networking connection.", mimetype="text/plain", status=500)