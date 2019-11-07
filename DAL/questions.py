import connection


@connection.connection_handler
def get_questions(cursor, column, order):
    cursor.execute(f"""
                    SELECT * FROM question
                    ORDER BY {column} {order}; 
                    """)
    all_questions = cursor.fetchall()
    return all_questions


@connection.connection_handler
def get_five_newest(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time DESC
                    LIMIT 5
                    """)
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def add_new(cursor, data):
    cursor.execute("""
                    INSERT INTO question ( view_number, vote_number, title, message, image)
                    VALUES 
                        (0,0,%(title)s,%(message)s,%(image)s);
                    """,
                   {
                       'title': data['title'],
                       'message': data['message'],
                       'image': data['image']})


@connection.connection_handler
def update(cursor, data):
    cursor.execute("""
                    UPDATE question
                    SET view_number = %(view_number)s,
                        vote_number = %(vote_number)s,
                        title = %(title)s,
                        message = %(message)s,
                        image = %(image)s
                    WHERE id = %(id)s;
                    """,
                   {
                       'view_number': data['view_number'],
                       'vote_number': data['vote_number'],
                       'title': data['title'],
                       'message': data['message'],
                       'image': data['image'],
                       'id': data['id']
                   })


@connection.connection_handler
def delete(cursor, data):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(id)s;
                    """,
                   {
                       'id': data['id']
                   })


@connection.connection_handler
def select_one(cursor, id_):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(id)s;
                    """,
                   {'id': id_})
    one_row = cursor.fetchone()
    return one_row

