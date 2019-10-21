import csv
import os

ANSWER_DATA_PATH = 'answer.csv'
QUESTION_DATA_PATH = 'question.csv'
ANSWER_HEADERS = ['id', 'submission_time', 'question_id', 'message']
QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'title', 'message']

def get_data_from_csv(csv_file, id=None ):
    all_data = []
    with open( csv_file, encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        single_data = dict(row)
        if id  is not None and id == single_data['id']:
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

def get_id(id):
    
