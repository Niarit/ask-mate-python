import connection


@connection.connection_handler
def add_new(cursor, tag):
    cursor.execute("""
                    INSERT INTO tag (name)
                    VALUES
                        ('%s');
                    """ % (tag['name']))


@connection.connection_handler
def get_all(cursor):
    cursor.execute("""
                    SELECT * FROM tag;
                    """)
    all_tags = cursor.fetchall()
    return all_tags


@connection.connection_handler
def get_all_for_a_question(cursor, question_id):
    cursor.execute("""
                    SELECT tag.* FROM question_tag
                    RIGHT JOIN tag
                    ON question_tag.tag_id = tag.id
                    WHERE question_id = %d;
                    """ % (question_id))
    all_tags = cursor.fetchall()
    return all_tags


@connection.connection_handler
def add_to_question(cursor, tag):
    cursor.execute("""
                    INSERT INTO question_tag (question_id, tag_id)
                    VALUES
                        (%s, %s);
                    """ % (tag['question_id'], tag['id']))


@connection.connection_handler
def remove_from_question(cursor, question_id, tag_id):
    cursor.execute("""
                    DELETE FROM question_tag
                    WHERE question_id=%d AND tag_id=%d
                    """ % (question_id, tag_id))
