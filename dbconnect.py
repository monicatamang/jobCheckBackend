import dbcreds
import mariadb
import traceback

# Creating a function that opens a database connection
def open_db_connection():
    # Trying to return the database connection
    try:
        return mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
    # Catching errors with the following exceptions
    except mariadb.OperationalError:
        traceback.print_exc()
        print("An unexpected error has occurred in the database. Failed to connect the database.")
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("An error has occurred in the database. Failed to connect to the database.")
    except:
        traceback.print_exc()
        print("Sorry, something went wrong. Please try again.")

# Creating a function that returns a cursor object using the current connection
def create_db_cursor(conn):
    # Trying to return the database cursor
    try:
        return conn.cursor()
    # Catching errors with the following exceptions
    except mariadb.InternalError:
        traceback.print_exc()
        print("An error has occurred in the database. The database cursor is no longer valid.")
    except mariadb.OperationalError:
        traceback.print_exc()
        print("An unexpected error has occurred. Failed to create cursor.")
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("Cannot connect to the database. Failed to create cursor.")
    except:
        traceback.print_exc()
        print("Sorry, something went wrong. Please try again.")

# Creating a function that closes the cursor
def close_cursor(cursor):
    # If the cursor was not created initially, don't close it and return True
    if(cursor == None):
        return True
    # Trying to close the database cursor
    try:
        cursor.close()
        # If the cursor closes, return True
        return True
    # Catching errors with the following exceptions and returning False
    except mariadb.InternalError:
        traceback.print_exc()
        print("An error has occurred in the database. The database cursor is no longer valid.")
        return False
    except mariadb.OperationalError:
        traceback.print_exc()
        print("An unexpected error has occurred in the database. Failed to close cursor")
        return False
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("An error has occurred in the database. Failed to close cursor")
        return False
    except:
        traceback.print_exc()
        print("Sorry, something went wrong. Please try again.")
        return False

# Creating a function that closes the database connection
def close_db_connection(conn):
    # If the database connection was not opened initially, don't close it and return True
    if(conn == None):
        return True
    # Trying to close the database connection
    try:
        conn.close()
        # If the database connection is closed, return True
        return True
    # Catching errors with the following exceptions and returning False
    except mariadb.OperationalError:
        traceback.print_exc()
        print("An unexpected error has occurred in the database. Failed to close database connection.")
        return False
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("An error has occurred in the database. Failed to close database connection.")
        return False
    except:
        traceback.print_exc()
        print("Sorry, something went wrong. Please try again.")
        return False