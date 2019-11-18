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
