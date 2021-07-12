from flask import Response
import mariadb
import dbconnect
import traceback
import dbcheck

def run_select_statement(sql, params):
    # Opening database and creating a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)
    # Initalizing the result as None
    result = None

    # Checking to see if the database connection and cursor are still open
    check_database = dbcheck.check_db_connection_and_cursor(conn, cursor)
    if(check_database == False):
        return Response("An error has occurred. Database connection and/or cursor are closed.", mimetype="text/plain", status=500)

    # Trying to run the SELECT statement with the sql and params passed in
    try:
        cursor.execute(sql, params)
        result = cursor.fetchall()
    except mariadb.DataError:
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
    # Returning the result
    return result

def run_insert_statement(sql, data):
    # Opening database and creating a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)
    # Initalizing the result as None
    result = None

    # Checking to see if the database connection and cursor are still open
    check_database = dbcheck.check_db_connection_and_cursor(conn, cursor)
    if(check_database == False):
        return Response("An error has occurred. Database connection and/or cursor are closed.", mimetype="text/plain", status=500)

    # Trying to run the INSERT statement with the sql and data passed in
    try:
        cursor.execute(sql, data)
        conn.commit()
        result = cursor.lastrowid
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
    # Returning the result
    return result

def run_update_statement(sql, data):
    # Opening database and creating a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)
    # Initalizing the result as None
    result = None

    # Checking to see if the database connection and cursor are still open
    check_database = dbcheck.check_db_connection_and_cursor(conn, cursor)
    if(check_database == False):
        return Response("An error has occurred. Database connection and/or cursor are closed.", mimetype="text/plain", status=500)

    # Trying to run the UPDATE statement with the sql and data passed in
    try:
        cursor.execute(sql, data)
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
    # Returning the result
    return result

def run_delete_statement(sql, data):
    # Opening database and creating a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)
    # Initalizing the result to None
    result = None

    # Checking to see if the database connection and cursor are still open
    check_database = dbcheck.check_db_connection_and_cursor(conn, cursor)
    if(check_database == False):
        return Response("An error has occurred. Database connection and/or cursor are closed.", mimetype="text/plain", status=500)

    # Trying to run the DELETE statment with the sql and data passed in
    try:
        cursor.execute(sql, data)
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
    # Returning the result
    return result