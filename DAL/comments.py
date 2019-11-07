import connection


@connection.connection_handler
def get_comments_for_a_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE question_id = %(question_id)s
                    ORDER BY id ASC;
                    """,
                   {
                       'question_id': question_id
                   })
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def add_new(cursor, data):
    cursor.execute("""
                    INSERT INTO comment (question_id, answer_id, message)
                    VALUES
                        (%(question_id)s, %(answer_id)s, %(message)s);
                    """,
                   {
                       'question_id': data['question_id'],
                       'answer_id': data['answer_id'],
                       'message': data['message'],
                   })


@connection.connection_handler
def select_one(cursor, comment_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE id = %(c_id)s
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
                        edited_count = %(edited_count)s
                    WHERE id= %(_id)s
                    """,
                   {
                       '_id': data['id'],
                       'message': data['message'],
                       'edited_count': data['edited_count']
                   })
