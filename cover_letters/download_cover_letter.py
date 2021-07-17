from flask import request, Response, send_from_directory
import dbstatements
import traceback
import json

# Creating a function that checks to see if the user is allowed to download their cover letter
def download_cv_file(name):
    # Trying to get the user's login token and cover letter id
    try:
        login_token = request.headers['Login-Token']
        cover_letter_id = int(request.args['coverLetterId'])

        # If the user sends a login token without content, send a client error response
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

    # Checking to see if the user's login token and cover letter id matches with the database records
    db_records = dbstatements.run_select_statement("SELECT us.token, cl.id FROM user_session us INNER JOIN cover_letter cl ON cl.user_id = us.user_id WHERE us.token = ? AND cl.id = ?", [login_token, cover_letter_id])

    # If the user's login token and resume id matches with the database records, send the user's resume
    if(len(db_records) == 1):
        # Trying to send the user's cover letter
        try:
            return send_from_directory("cover_letter_uploads/", name, as_attachment=True)
        except FileNotFoundError:
            traceback.print_exc()
            return Response("File not found.", mimetype="text/plain", status=403)
        except:
            traceback.print_exc()
            return Response("Something went wrong. Please refresh the page.", mimetype="text/plain", status=403)
    # If the user's login token and cover letter id does not match with the database records, send a client error response
    else:
        return Response("Failed to download cover letter.", mimetype="text/plain", status=403)

# Creating a function that get's the user's cover letter filename from the database
def get_cv_filename_from_db():
    # Trying to get the user's login token and cover letter id
    try:
        login_token = request.headers['Login-Token']
        cover_letter_id = int(request.args['coverLetterId'])

        # If the user sends a login token without content, send a client error response
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

    # Getting the user's cover letter filename from the database given the login token and cover letter id
    cv_filename_list = dbstatements.run_select_statement("SELECT cl.cover_letter_file FROM user_session us INNER JOIN cover_letter cl ON cl.user_id = us.user_id WHERE us.token = ? AND cl.id = ?", [login_token, cover_letter_id])

    # If the cover letter filename is retrieved from the database, convert the cover letter filename into JSON data
    if(len(cv_filename_list) == 1):
        cv_filename_json = json.dumps(cv_filename_list[0][0])
        # Returning a client success response with the JSON data
        return Response(cv_filename_json, mimetype="application/json", status=200)
    # If the cover letter filename is not retrieved from the database, send a server error response
    else:
        return Response("Failed to retrieve cover letter.", mimetype="text/plain", status=500)