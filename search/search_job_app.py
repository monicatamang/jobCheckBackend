from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that will return the user's job applications based on the company's name
def search_job_app():
    # Trying to get the user's id and search input
    try:
        user_id = int(request.args['userId'])
        search_input = request.args['searchInput']

        # If the user sends their id and search input without content, send a client error response
        if(search_input == ''):
            return Response("Please enter a valid search input.", mimetype="text/plain", status=403)
    except ValueError:
        traceback.print_exc()
        return Response("Invalid data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        return Response("Incorrect or missing key.", mimetype="text/plain", status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong. Please try again.", mimetype="text/plain", status=400)

    # If the user does not send any data, return a client error response
    if(search_input == None):
        return Response("Please enter a valid search input.", mimetype="text/plain", status=400)
    # If the user does send data, try to find all the user's job applications that matches or closely matches with their search input
    else:
        results = dbstatements.run_select_statement("SELECT id, company, job_posting_url, job_position, job_location, employment_type, salary_type, salary_amount, start_date, due_date, status, applied_date, notes FROM job_application WHERE user_id = ? AND company LIKE CONCAT('%', ?, '%') ORDER BY created_at DESC", [user_id, search_input])

    # If a database error occurs, send a server error response
    if(results == None):
        return Response(f"Failed to find '{search_input}'.", mimetype="text/plain", status=500)
    # If a match is found, send all matches as a list of dictionaries
    # If no matches are found, an empty list will be returned
    else:
        search_results = []
        for result in results:
            each_result = {
                'userId': user_id,
                'jobAppId': result[0],
                'company': result[1],
                'jobPostingUrl': result[2],
                'jobPosition': result[3],
                'jobLocation': result[4],
                'employmentType': result[5],
                'salaryType': result[6],
                'salaryAmount': result[7],
                'jobStartDate': result[8],
                'dueDate': result[9],
                'status': result[10],
                'appliedDate': result[11],
                'notes': result[12]
            }
            search_results.append(each_result)
        # Convert data into JSON
        search_results_json = json.dumps(search_results, default=str)
        # Send a client success response with the JSON data
        return Response(search_results_json, mimetype="application/json", status=200)