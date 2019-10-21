import csv
import time

ANSWER_DATA_PATH = 'answer.csv'
QUESTION_DATA_PATH = 'question.csv'
ANSWER_HEADERS = ['id', 'submission_time', 'question_id', 'message']
QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'title', 'message']


def get_data_from_csv(csv_file, qa_id=None):
    all_data = []
    with open(csv_file, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            single_data = dict(row)
            if qa_id is not None and qa_id == single_data['id']:
                return single_data
            all_data.append(single_data)
    return all_data


def get_all_data(csv_file, break_lines=False):
    all_data = get_data_from_csv(csv_file)
    if break_lines:
        for data in all_data:
            data['message'] = convert_enter_to_br(data['message'])
    return all_data


def convert_enter_to_br(original_string):
    return '<br>'.join(original_string.split('\n'))


def get_id(_id):
    return get_data_from_csv(_id)


def creat_new_id(csv_file):
    existing_data = get_data_from_csv(csv_file)
    if len(existing_data) == 0:
        return'1'
    return str(int(existing_data[-1]['id'])+1)


def add_new_question(question):
    question['id'] = creat_new_id(QUESTION_DATA_PATH)
    question['submission_time'] = get_submission_time()
    add_new_question_to_file(question, True)


def add_new_question_to_file(question, append=True):
    existing_data = get_all_data(QUESTION_DATA_PATH)
    with open(QUESTION_DATA_PATH, 'w', newline='', encoding='utf-8') as questions:
        writer = csv.DictWriter(questions, fieldnames=QUESTION_HEADERS)
        writer.writeheader()
        for row in existing_data:
            if not append:
                if row['id'] == question['id']:
                    row = question
            writer.writerow(row)
            if append:
                writer.writerow(question)


def get_submission_time():
    return int(time.time())

>>>>>>> 70286f66bacfc3859250c28147fc1498ff1718b6
