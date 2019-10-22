import csv
import time

ANSWER_DATA_PATH = 'answer.csv'
QUESTION_DATA_PATH = 'question.csv'
ANSWER_HEADERS = ['id', 'submission_time','vote_number', 'question_id', 'message','image']
QUESTION_HEADERS = ['id', 'submission_time', 'view_number','vote_number', 'title', 'message', 'image']


def get_data_from_csv(csv_file, qa_id=None):
    with open(csv_file, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        all_data = list(reader)
        if qa_id:
            for row in all_data:
                single_data = dict(row)
                if qa_id == single_data['id']:
                    return single_data
    return all_data


def get_all_data(csv_file, break_lines=False):
    all_data = get_data_from_csv(csv_file)
    if break_lines:
        for data in all_data:
            data['message'] = convert_enter_to_br(data['message'])
    return all_data


def convert_enter_to_br(original_string):
    return '<br>'.join(original_string.split('\n'))


def get_id(file_name, _id):
    return get_data_from_csv(file_name, _id)


def creat_new_id(csv_file):
    existing_data = get_data_from_csv(csv_file)
    if len(existing_data) == 0:
        return'1'
    return str(int(existing_data[-1]['id'])+1)


def add_new_question(question):
    question['id'] = creat_new_id(QUESTION_DATA_PATH)
    question['submission_time'] = get_submission_time()
    add_new_data_to_file(question, QUESTION_DATA_PATH, QUESTION_HEADERS)


def add_new_data_to_file(data, file_to, header):
    with open(file_to, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writerow(data)


def add_new_message(answer, question_id):
    answer = dict(answer)
    answer['id'] = creat_new_id(ANSWER_DATA_PATH)
    answer['submission_time'] = get_submission_time()
    answer['question_id'] = question_id
    add_new_data_to_file(answer, ANSWER_DATA_PATH, ANSWER_HEADERS)


def get_submission_time():
    return int(time.time())


def edit_question(data, file_to):
    update_existing_file(data, file_to, QUESTION_HEADERS)


def question_vote_up(data):
    update_existing_file(data, QUESTION_DATA_PATH, QUESTION_HEADERS)


def update_existing_file(data, file_to, header):
    with open(file_to, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
