from flask import request, Response
import traceback
import dbstatements

# Creating a function that deletes a user's cover letter
def delete_cover_letter_file():
    # Trying to get the user's id and cover letter id
    try:
        login_token = request.json['loginToken']
        cover_letter_id = int(request.json['coverLetterId'])

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

    # Checking to see if the user's cover letter is deleted from the database
    row_count = dbstatements.run_delete_statement("DELETE cv FROM user_session us INNER JOIN cover_letter cv ON cv.user_id = us.user_id WHERE us.token = ? AND cv.id = ?", [login_token, cover_letter_id])

    # If the cover letter is deleted from the database, send a client success response
    if(row_count == 1):
        return Response(status=204)
    # If the cover letter is not deleted from the database, send a server error response
    else:
        return Response("Failed to delete cover letter.", mimetype="text/plain", status=500)