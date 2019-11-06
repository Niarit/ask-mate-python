import connection


@connection.connection_handler
def get_answers(cursor):
    cursor.execute("""
                    SELECT * FROM answer;
                    """)
    all_answers = cursor.fetchall()
    return all_answers


@connection.connection_handler
def get_answers_for_a_question(cursor, q_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(q_id)s
                    """,
                   {
                       'q_id': q_id
                   })
    answers = cursor.fetchall()
    return answers

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


@connection.connection_handler
def delete(cursor, data):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE id = %(id)s;
                    """,
                   {
                       'id': data['id']
                   })


@connection.connection_handler
def select_one(cursor, id_):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(id)s;
                    """,
                   {'id': id_})
    one_row = cursor.fetchone()
    return one_row
