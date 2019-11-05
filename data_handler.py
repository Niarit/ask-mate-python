import connection


# def add_new_question(question):
#     question['id'] = connection.creat_new_id(QUESTION_DATA_PATH)
#     question['submission_time'] = connection.get_submission_time()
#     question['vote_number'] = 0
#     question['view_number'] = 0
#     add_new_data_to_file(question, QUESTION_DATA_PATH, QUESTION_HEADERS)


# def add_new_data_to_file(data, file_to, header):
#     with open(file_to, 'a', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=header)
#         writer.writerow(data)


# def add_new_message(answer, question_id):
#     answer = dict(answer)
#     answer['id'] = connection.creat_new_id(ANSWER_DATA_PATH)
#     answer['submission_time'] = connection.get_submission_time()
#     answer['question_id'] = question_id
#     answer['vote_number'] = 0
#     add_new_data_to_file(answer, ANSWER_DATA_PATH, ANSWER_HEADERS)


# def edit_question(data, file_to):
#     update_existing_file(data, file_to, QUESTION_HEADERS)


def question_vote_update(data):
    update_existing_file(data, QUESTION_DATA_PATH, QUESTION_HEADERS)


def update_existing_file(data, file_to, header):
    with open(file_to, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def get_row_index_by_id(id_to_find, data):
    id_to_find = int(id_to_find)
    for index, row in enumerate(data):
        if row['id'] == id_to_find:
            return index


def save_answers(answers):
    update_existing_file(answers, ANSWER_DATA_PATH, ANSWER_HEADERS)


def insert_answer(answer):
    """
    :param answer: (dict)
    :return: (None)
    """

    answer['id'] = connection.creat_new_id(ANSWER_DATA_PATH)
    answer['submission_time'] = connection.get_submission_time()
    answer['vote_number'] = 0
    add_new_data_to_file(answer, 'answer.csv', ANSWER_HEADERS)


def save_questions(questions):
    update_existing_file(questions, QUESTION_DATA_PATH, QUESTION_HEADERS)