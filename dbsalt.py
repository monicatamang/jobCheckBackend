import dbstatements
import string
import random

# Creating a function that will generate salt
def create_salt():
    # Creating salt as 10 random characters
    letters_and_digits = string.ascii_letters + string.digits
    salt = ''.join((random.choice(letters_and_digits) for i in range(10)))
    # Return salt
    return salt

# Creating a function that will get the user's salt from the database given the user's email
def get_salt(email):
    # Trying to get the salt from the database
    salt_list = dbstatements.run_select_statement("SELECT salt FROM users WHERE email = ?", [email,])
    # If the user's salt is retrieved from the database, return salt
    if(len(salt_list) == 1):
        return salt_list[0][0]
    # If the user's salt is not retrieved from the database, return None
    else:
        return None