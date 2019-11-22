import connection


@connection.connection_handler
def get_answers(cursor):
    cursor.execute("""
                    SELECT answer.id, 
                        submission_time, 
                        vote_number,
                        question_id,
                        message, 
                        image,
                        user_id,
                        users.user_name 
                        FROM answer
                    JOIN users ON answer.user_id = users.id;
                    """)
    all_answers = cursor.fetchall()
    return all_answers


@connection.connection_handler
def get_answers_for_a_question(cursor, q_id):
    cursor.execute("""
                    SELECT
                        answer.*,
                        accepted_answers.answer_id AS is_accepted,
                        users.user_name
                    FROM answer
                    LEFT JOIN accepted_answers ON answer.id = accepted_answers.answer_id
                    JOIN users ON answer.user_id = users.id
                    WHERE answer.question_id = %(q_id)s
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
def add_new(cursor, data, user_id):
    cursor.execute("""
                    INSERT INTO answer (vote_number, question_id, message, image, user_id)
                    VALUES 
                        (0,%(question_id)s,%(message)s,%(image)s,%(user_id)s);
                    """,
                   {
                       'question_id': data['question_id'],
                       'message': data['message'],
                       'image': data['image'],
                       'user_id': user_id
                   })


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
                    SELECT answer.id, 
                        submission_time, 
                        vote_number,
                        question_id,
                        message, 
                        image,
                        user_id,
                        users.user_name 
                        FROM answer
                    JOIN users ON answer.user_id = users.id
                    WHERE answer.id = %(id)s;
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


@connection.connection_handler
def get_users_answers(cursor, user_id):
    cursor.execute("""
                    SELECT question.title,
                        answer.message,
                        answer.submission_time,
                        answer.vote_number, 
                        answer.question_id FROM answer
                    JOIN question ON answer.question_id = question.id
                    WHERE answer.user_id = %(user_id)s""",
                   {
                       'user_id': user_id
                   })
    users_answers = cursor.fetchall()
    return users_answers
