import connection


@connection.connection_handler
def add_user(cursor, data):
    cursor.execute("""
                    INSERT INTO users (user_name, pw)
                    VALUES (%(user_name)s, %(pw)s)""",
                   {
                       'user_name' : data['user_name'],
                       'pw' : data['password']
                   })


@connection.connection_handler
def get_all_users(cursor):
    cursor.execute("""
                    SELECT id, user_name FROM users""")
    all_users = cursor.fetchall()
    return all_users
