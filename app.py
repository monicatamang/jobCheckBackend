from flask import Flask
from users import create_user, update_user, delete_user
from login import create_login, delete_login
from job_applications import get_job_app, create_job_app, update_job_app, delete_job_app
from interviews import get_interview, create_interview, update_interview, delete_interview
from interviewers import get_interviewer, create_interviewer, update_interviewer, delete_interviewer
from job_references import get_job_reference, create_job_reference, update_job_reference, delete_job_reference
from networking_events import get_networking_event, create_networking_event, update_networking_event, delete_networking_event
from networking_connections import get_connection, create_connection, update_connection, delete_connection
from resume import upload_resume, delete_resume, download_resume
import sys

app = Flask(__name__)

# Limiting the maximum allowed payload to be 10MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000

# Creating a POST request that will sign up a user
@app.post("/api/users")
def call_signup_user():
    return create_user.signup_user()

# Creating a PATCH request that will update a user
@app.patch("/api/users")
def call_update_user():
    return update_user.update_user()

# Creating a DELETE request that will delete a user
@app.delete("/api/users")
def call_delete_user():
    return delete_user.delete_user()

# Creating a POST request that will log in a user
@app.post("/api/login")
def call_login_user():
    return create_login.login_user()

# Creating a DELETE request that will log out a user
@app.delete("/api/login")
def call_logout_user():
    return delete_login.logout_user()

# Creating a GET request that will get a user's job applications
@app.get("/api/job-applications")
def call_get_job_app():
    return get_job_app.get_job_app()

# Creating a POST request that will create a job application
@app.post("/api/job-applications")
def call_create_job_app():
    return create_job_app.create_job_app()

# Creating a PATCH request that will update a user's job application
@app.patch("/api/job-applications")
def call_update_job_app():
    return update_job_app.update_job_app()

# Creating a DELETE request that will delete a user's job application
@app.delete("/api/job-applications")
def call_delete_app():
    return delete_job_app.delete_job_app()

# Creating GET request that will get a user's interviews
@app.get("/api/interviews")
def call_get_interviews():
    return get_interview.get_interviews()

# Creating POST request that will create an interview
@app.post("/api/interviews")
def call_create_interview():
    return create_interview.create_interview()

# Creating PATCH request that will update an interview
@app.patch("/api/interviews")
def call_update_interview():
    return update_interview.update_interview()

# Creating DELETE request that will delete an interview
@app.delete("/api/interviews")
def call_delete_interview():
    return delete_interview.delete_interview()

# Creating a GET request that will get a user's interviewers
@app.get("/api/interviewers")
def call_get_interviewer():
    return get_interviewer.get_interviewers()

# Creating a POST request that will create an interviewer
@app.post("/api/interviewers")
def call_create_interviewer():
    return create_interviewer.create_interviewer()

# Creating a PATCH request that will update an interviewer
@app.patch("/api/interviewers")
def call_update_interviewer():
    return update_interviewer.update_interviewer()

# Creating a DELETE request that will delete an interviewer
@app.delete("/api/interviewers")
def call_delete_interviewer():
    return delete_interviewer.delete_interviewer()

# Creating a GET request that will get a user's job references
@app.get("/api/job-references")
def call_get_job_ref():
    return get_job_reference.get_job_ref()

# Creating a POST request that will create a job reference
@app.post("/api/job-references")
def call_create_job_ref():
    return create_job_reference.create_job_ref()

# Creating a PATCH request that will update a job reference
@app.patch("/api/job-references")
def call_update_job_ref():
    return update_job_reference.update_job_ref()

# Creating a DELETE request that will delete a job reference
@app.delete("/api/job-references")
def call_delete_job_ref():
    return delete_job_reference.delete_job_ref()

# Creating a GET request that will get a user's networking events
@app.get("/api/networking-events")
def call_get_networking_event():
    return get_networking_event.get_networking_events()

# Creating a POST request that will create a networking event
@app.post("/api/networking-events")
def call_create_networking_event():
    return create_networking_event.create_networking_event()

# Creating a PATCH request that will update a networking event
@app.patch("/api/networking-events")
def call_update_networking_event():
    return update_networking_event.update_networking_event()

# Creating a DELETE request that will delete a networking event
@app.delete("/api/networking-events")
def call_delete_networking_event():
    return delete_networking_event.delete_networking_event()

# Creating a GET request that will get a user's networking connections
@app.get("/api/networking-connections")
def call_get_networking_connections():
    return get_connection.get_networking_connections()

# Creating a POST request that will create a networking connection
@app.post("/api/networking-connections")
def call_create_networking_connection():
    return create_connection.create_networking_connection()

# Creating a PATCH request that will update a networking connection
@app.patch("/api/networking-connections")
def call_update_networking_connection():
    return update_connection.update_networking_connection()

# Creating a DELETE request that will delete a networking connection
@app.delete("/api/networking-connections")
def call_delete_networking_connection():
    return delete_connection.delete_networking_connection()

# Creating a POST request that will allow user's to upload their resume
@app.post('/api/upload-resume')
def call_upload_file():
    return upload_resume.store_resume_file()

# Creating a DELETE request that will delete a user's resume
@app.delete('/api/delete-resume')
def call_delete_file():
    return delete_resume.delete_resume_file()

# Creating a POST request that will allow user's to download their resume
@app.post('/api/download-resume')
def call_download_file():
    return download_resume.get_resume_from_db()

# Creating a mode
# If more than one argument is passed, set the second argument as the mode
if(len(sys.argv) > 1):
    mode = sys.argv[1]
# If no mode is passed, print a message and exit the application
else:
    print("No mode argument, please pass a mode argument when invoking the file")
    exit()

# Checking which mode is used
# If the application runs in "production" mode, import bjoern and run the application on port 5005
if(mode == "production"):
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5005)
# If the application runs in "testing" mode, import CORS with debug mode turned on
elif(mode == "testing"):
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
# If the application is not passed a valid mode, print a message and exit the application
else:
    print("Invalid mode, please select either 'production' or 'testing'")
    exit()