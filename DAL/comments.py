import connection


@connection.connection_handler
def get_comments_for_a_question(cursor, question_id):
    cursor.execute("""
                    SELECT comment.id,
                        question_id,
                        answer_id,
                        message,
                        submission_time,
                        edited_count,
                        user_id,
                        users.user_name 
                        FROM comment
                    JOIN users ON comment.user_id = users.id
                    WHERE question_id = %(question_id)s
                    ORDER BY id ASC;
                    """,
                   {
                       'question_id': question_id
                   })
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def add_new(cursor, data, user_id):
    cursor.execute("""
                    INSERT INTO comment (question_id, answer_id, message, user_id)
                    VALUES
                        (%(question_id)s, %(answer_id)s, %(message)s, %(user_id)s);
                    """,
                   {
                       'question_id': data['question_id'],
                       'answer_id': data['answer_id'],
                       'message': data['message'],
                       'user_id': user_id
                   })


@connection.connection_handler
def select_one(cursor, comment_id):
    cursor.execute("""
                    SELECT comment.id,
                        question_id,
                        answer_id,
                        message,
                        submission_time,
                        edited_count,
                        user_id,
                        users.user_name 
                        FROM comment
                    JOIN users ON comment.user_id = users.id
                    WHERE comment.id = %(c_id)s
                    """,
                   {
                       'c_id': comment_id,
                   })
    one_row = cursor.fetchone()
    return one_row


@connection.connection_handler
def update(cursor, data):
    cursor.execute("""
                    UPDATE comment
                    SET message = %(message)s,
                        submission_time = %(submission_time)s,
                        edited_count = %(edited_count)s
                    WHERE id= %(_id)s
                    """,
                   {
                       '_id': data['id'],
                       'message': data['message'],
                       'submission_time': data['submission_time'],
                       'edited_count': data['edited_count']
                   })


@connection.connection_handler
def delete_from_question(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(id)s
                    RETURNING question_id, answer_id;
                    """,
                   {
                       'id': comment_id
                   })
    question_id = cursor.fetchone()
    return question_id


@connection.connection_handler
def get_comments_for_an_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT comment.id,
                        question_id,
                        answer_id,
                        message,
                        submission_time,
                        edited_count,
                        user_id,
                        users.user_name 
                        FROM comment
                    JOIN users ON comment.user_id = users.id
                    WHERE answer_id = %(answer_id)s
                    ORDER BY id ASC;
                    """,
                   {
                       'answer_id': answer_id
                   })
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def get_users_comments_for_answers(cursor, user_id):
    cursor.execute("""
                    SELECT comment.message, answer.question_id, comment.submission_time FROM comment
                    JOIN answer ON comment.answer_id = answer.id
                    WHERE comment.user_id = %(user_id)s""",
                   {
                       'user_id': user_id
                   })
    users_answer_comments = cursor.fetchall()
    return users_answer_comments


@connection.connection_handler
def get_users_comments_for_questions(cursor, user_id):
    cursor.execute("""
                    SELECT comment.question_id, comment.message, comment.submission_time FROM comment
                    JOIN question ON comment.question_id = question.id
                    WHERE comment.user_id = %(user_id)s""",
                   {
                       'user_id': user_id
                   })
    users_question_comments = cursor.fetchall()
    return users_question_comments
