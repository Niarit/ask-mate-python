"""
Helper functions which can be called from any other layer. (but mainly from the business logic layer)
"""

import server
import data_handler


def vote_answer(answer_id, direction):
    answers = data_handler.get_all_data('answer.csv', True)
    answer_row_index = server.get_row_index_by_id(answer_id, answers)
    if answer_row_index is None:
        raise ValueError(f'Answer {{ID: {answer_id}}} not found!')
    answer = answers[answer_row_index]
    answer['vote_number'] = direction(answer['vote_number'])
    data_handler.save_answers(answers)
    return answer
