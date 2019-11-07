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
                    ORDER BY id ASC;
                    """,
                   {
                       'q_id': q_id
                   })
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def add_answer(cursor, q_id, data):
    cursor.execute("""
                    INSERT INTO answer (vote_number, question_id, message, image)
                    VALUES (0, %(q_id)s, %(message)s, %(image)s)
                    """,
                   {
                       'q_id': q_id,
                       'message': data['message'],
                       'image': data['image']
                   })


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
                    SET message = %(message)s,
                        vote_number = %(vote_number)s
                    WHERE id = %(id)s;
                    """,
                   {
                       'message': data['message'],
                       'id': data['id'],
                       'vote_number': data['vote_number']
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


@connection.connection_handler
def get_question_id_from_answer(cursor, ans_id):
    cursor.execute("""
                    SELECT question_id FROM answer
                    WHERE id = %(ans_id)s
                    """,
                   {
                       'ans_id': ans_id
                   })
    one_row = cursor.fetchone()
    return one_row
