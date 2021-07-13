from flask import Flask
from users import create_user, update_user, delete_user
from login import create_login, delete_login
from job_applications import get_job_app, create_job_app, update_job_app, delete_job_app
from interviews import create_interview, update_interview
import sys

app = Flask(__name__)

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

# Creating POST request that will create an interview
@app.post("/api/interviews")
def call_create_interview():
    return create_interview.create_interview()

# Creating PATCH request that will update an interview
@app.patch("/api/interviews")
def call_update_interview():
    return update_interview.update_interview()

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
    print("Invalid mode, please select either 'production' or 'testing'.")
    exit()