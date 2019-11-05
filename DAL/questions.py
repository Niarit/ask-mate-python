import connection


@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    """)
    all_questions = cursor.fetchall()
    return all_questions


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
                    WHERE id = %(question_id)s;
                    """,
                   {
                       'view_number': data['view_number'],
                       'vote_number': data['vote_number'],
                       'title': data['title'],
                       'message': data['message'],
                       'image': data['image'],
                       'question_id': data['question_id']
                   })

