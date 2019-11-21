"""
Module to validate user input.
"""


def as_question(question):
    error_bag = []

    if question['title']:
        if len(question['title']) < 6:
            error_bag.append('The title of the question has to be at least 6 characters long!')
    else:
        error_bag.append('Please specify the question title!')

    if question['message']:
        if len(question['message']) < 10:
            error_bag.append('The content of the question has to be at least 10 characters long!')
    else:
        error_bag.append('Please specify the question message!')

    return error_bag


def as_search_query(query_form):
    error_bag = []

    if 'q' in query_form:
        if len(query_form['q']) < 2:
            error_bag.append('The search query has to be at least 2 characters long!')
    else:
        error_bag.append('Please specify the search query!')

    return error_bag
