from flask_mysqldb import MySQL
import MySQLdb.cursors, pickle
import base64 

mysql = MySQL()

def query(query, args=(), one=False):
    cursor = mysql.connection.cursor()
    cursor.execute(query, args)
    rv = [dict((cursor.description[idx][0], value)
        for idx, value in enumerate(row)) for row in cursor.fetchall()]
    return (rv[0] if rv else None) if one else rv


def login_user_db(username, password):
    user = query('SELECT username FROM users WHERE username = %s AND password = %s', (username, password,), one=True)
    
    if user:
        pickled_data = base64.b64encode(pickle.dumps(user))
        return pickled_data.decode("ascii") 
    else:
        return False

def register_user_db(username, password):
    check_user = query('SELECT username FROM users WHERE username = %s', (username,), one=True)

    if not check_user:
        query('INSERT INTO users(username, password) VALUES(%s, %s)', (username, password,))
        mysql.connection.commit()
        
        return True
    
    return False