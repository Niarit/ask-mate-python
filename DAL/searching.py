import connection


@connection.connection_handler
def in_questions(cursor, phrase):
    cursor.execute("""
                    SELECT question.* FROM question
                    FULL OUTER JOIN answer
                    ON question.id = answer.question_id
                    WHERE question.message LIKE %(phrase)s
                        OR question.title LIKE %(phrase)s
                        OR answer.message LIKE %(phrase)s
                    GROUP BY question.id;
                    """,
                   {
                       'phrase': '%' + phrase + '%'
                   })
    results = cursor.fetchall()
    return results


# @connection.connection_handler
