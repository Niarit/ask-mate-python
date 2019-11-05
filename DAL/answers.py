import connection


@connection.connection_handler
def get_answers(cursor):
    cursor.execute("""
                    SELECT * FROM answer;
                    """)
    all_answers = cursor.fetchall()
    return all_answers


@connection.connection_handler
def add_new(cursor, data):
    cursor.execute("""
                    INSERT INTO answer (vote_number, question_id, message, image)
                    VALUES 
                        (0,%(question_id)s,%(message)s,%(image)s);
                    """,
                   {
                       'question_id': data['question_id'],
                       'message': data['message'],
                       'image': data['image']})


@connection.connection_handler
def update(cursor, data):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = %(vote_number)s,
                        message = %(message)s,
                        image = %(image)s
                    WHERE id = %(id)s;
                    """,
                   {
                       'vote_number': data['vote_number'],
                       'message': data['message'],
                       'image': data['image'],
                       'id': data['id']
                   })

