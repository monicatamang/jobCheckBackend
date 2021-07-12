from flask import Response
import mariadb
import traceback
import dbconnect
import dbcheck
import secrets

def create_user_token(user_id):
    # Opening the database and creating a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)
    # Initalizing the result to None and create a token
    result = None
    token = secrets.token_urlsafe(60)

    # Checking to see if the database connection and cursor are still open
    check_database = dbcheck.check_db_connection_and_cursor(conn, cursor)
    if(check_database == False):
        return Response("An error has occurred. Database connection and/or cursor are closed.", mimetype="text/plain", status=500)

    # Trying to insert the new token into the database
    try:
        cursor.execute("INSERT INTO user_session(user_id, token) VALUES(?, ?)", [user_id, token])
        conn.commit()
        result = cursor.rowcount
    except mariadb.DataError:
        traceback.print_exc()
    except mariadb.IntegrityError:
        traceback.print_exc()
    except mariadb.OperationalError:
        traceback.print_exc()
    except mariadb.ProgrammingError:
        traceback.print_exc()
    except mariadb.DatabaseError:
        traceback.print_exc()
    except:
        traceback.print_exc()

    # Closing the cursor and database connection
    dbcheck.close_db_connection_and_cursor(conn, cursor)

    # If a new row is created in the 'user_session' table, return the token
    if(result == 1):
        return token
    # If a new row is not created, return None
    else:
        return None