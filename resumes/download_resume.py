from flask import request, Response, send_from_directory
import dbstatements
import traceback

def download_resume_file(name):
    try:
        return send_from_directory(f"resume_uploads/{name}", name, as_attachment=True)
    except FileNotFoundError:
        traceback.print_exc()
        return Response("File not found.", mimetype="text/plain", status=403)
    except:
        traceback.print_exc()
        return Response("Something went wrong. Please refresh the page.", mimetype="text/plain", status=403)

def get_resume_from_db():
    try:
        login_token = request.args['loginToken']
        resume_id = int(request.args['resumeId'])

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

    resume_filename_list = dbstatements.run_select_statement("SELECT r.resume_file FROM user_session us INNER JOIN resume r ON r.user_id = us.user_id WHERE us.token = ? AND r.id = ?", [login_token, resume_id])

    if(len(resume_filename_list) == 1):
        print(resume_filename_list[0][0])
        download_resume_file(resume_filename_list[0][0])
    else:
        return Response("Failed to download resume.", mimetype="text/plain", status=500)