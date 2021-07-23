from flask import request, Response
import traceback
import dbstatements
import os
from cover_letters import upload_cover_letter

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

    # Getting the cover letter file from the database given the login token and cover letter id
    cover_letter_file_list = dbstatements.run_select_statement("SELECT cl.cover_letter_file FROM user_session us INNER JOIN cover_letter cl ON cv.user_id = us.user_id WHERE us.token = ? AND cl.id = ?", [login_token, cover_letter_id])

    # If the resume file is retrieved from the database, check to see fi the user's cover letter exists in the 'cover_letter_upload' folder
    if(len(cover_letter_file_list) == 1):
        filename = os.path.join(upload_cover_letter.UPLOAD_FOLDER, cover_letter_file_list[0][0])
        # If the user's cover letter exists in the folder, remove the resume from the folder and database
        if(os.path.exists(filename)):
            os.remove(filename)
            # Checking to see if the user's cover letter is deleted from the database
            row_count = dbstatements.run_delete_statement("DELETE cl FROM user_session us INNER JOIN cover_letter cl ON cv.user_id = us.user_id WHERE us.token = ? AND cl.id = ?", [login_token, cover_letter_id])
            # If the cover letter is deleted from the database, send a client success response
            if(row_count == 1):
                return Response(status=204)
            # If the cover letter is not deleted from the database, send a server error response
            else:
                return Response("Failed to delete cover letter.", mimetype="text/plain", status=500)
        # If the user's cover letter does not exist in the folder, send a server error response
        else:
            return Response("Cover letter does not exist.", mimetype="text/plain", status=500)
    # If the cover letter file is not retrieved from the database, send a client error response
    else:
        return Response("User is not logged in.", mimetype="text/plain", status=403)