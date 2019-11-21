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
def edit_user(cursor, user_data, user_id):
    cursor.execute("""
                    UPDATE users
                    SET user_name = %(user_name)s,
                        pw = %(user_pw)s 
                    WHERE id = %(user_id)s""",
                   {
                       'user_name': user_data['user_name'],
                       'user_pw': user_data['password'],
                       'user_id': user_id
                   })


@connection.connection_handler
def get_password(cursor, user):
    cursor.execute("""
                    SELECT pw FROM users
                    WHERE user_name = %(user)s
                    """,
                   {
                       'user': user
                   })
    data = cursor.fetchone()
    return data


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


@connection.connection_handler
def get_user_rep(cursor, user_id):
    cursor.execute("""
                    SELECT reputation FROM users
                    WHERE id = %(user_id)s""",
                   {
                       'user_id': user_id
                   })
    reputation = cursor.fetchone()
    return reputation

