import csv
import time


def get_all_data(csv_file, break_lines=True):
    with open(csv_file, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        all_data = list(reader)
        for row in all_data:
            if break_lines:
                row['message'] = convert_enter_to_br(row['message'])
            for key, val in row.items():
                if is_number(val):
                    row[key] = int(val)
        return all_data


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        pass
    return False


def convert_enter_to_br(original_string):
    return '<br>'.join(original_string.split('\n'))


def get_submission_time():
    return int(time.time())


def creat_new_id(csv_file):
    existing_data = get_all_data(csv_file)
    if len(existing_data) == 0:
        return'1'
    return str(int(existing_data[-1]['id'])+1)


