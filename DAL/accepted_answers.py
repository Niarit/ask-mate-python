import connection


@connection.connection_handler
def add(cursor, question_id, answer_id):
    cursor.execute("""
                    INSERT INTO accepted_answers
                        (question_id, answer_id)
                    VALUES
                        (%(question_id)s, %(answer_id)s);
                    """,
                   {
                       'question_id': question_id,
                       'answer_id': answer_id,
                   })
