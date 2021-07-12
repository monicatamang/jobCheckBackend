import re

# Creating a function that will check if a user's email is valid
def check_email_format(test_email):
    # Checking to see if the user's email matches the pattern for a valid email
    valid_email = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+').search(test_email)
    # If the user's email is valid, return True
    if(valid_email):
        return True
    # If the user's email is not valid, return False
    return False