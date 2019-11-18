import connection


@connection.connection_handler
def add_user(cursor, data):
    cursor.execute("""
                    INSERT INTO users (user_name, pw)
                    VALUES (%(user_name)s, %(pw)s)""",
                   {
                       'user_name': data['user_name'],
                       'pw': data['password']
                   })


@connection.connection_handler
def get_all_users(cursor):
    cursor.execute("""
                    SELECT id, user_name FROM users""")
    all_users = cursor.fetchall()
    return all_users


@connection.connection_handler
def edit_user(cursor, user_data):
    cursor.execute("""
                    UPDATE users
                    SET user_name = %(user_name)s,
                        pw = %(user_pw)s """,
                   {
                       'user_name': user_data['user_name'],
                       'user_pw': user_data['password']
                   })


@connection.connection_handler
def get_one_user(cursor, user_name):
    cursor.execute("""
                    SELECT * FROM users
                    WHERE user_name = %(user_name)s""",
                   {
                       'user_name': user_name
                   })
    user_data = cursor.fetchone()
    return user_data
