import DAL.accepted_answers
import DAL.answers
import DAL.comments
import DAL.questions
import DAL.searching
import DAL.tags
import DAL.users
import os
import uuid
import time
from datetime import datetime
import bcrypt


__ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def search(request):
    phrase = request.args.get('q')
    question_ids = DAL.searching.in_questions(phrase)
    return question_ids


def route_five_list():
    data = DAL.questions.get_five_newest()
    return data


def route_list(request):
    order_direction = 'DESC'
    if 'order_direction' in request.args:
        order_direction = request.args.get('order_direction')
    column_name = 'submission_time'
    if 'order_by' in request.args:
        column_name = request.args.get('order_by')
    sorted_questions = DAL.questions.get_questions(column_name, order_direction)
    if order_direction == 'DESC':
        order_direction = 'ASC'
    else:
        order_direction = 'DESC'
    return sorted_questions, order_direction


def add_question(request, upload_image_func, app, session):
    request_form = dict(request.form)
    session['id'] = DAL.users.get_one_user(session['username'])['id']
    __upload_file_if_any(request, request_form, upload_image_func, app)
    DAL.questions.add_new(request_form, session['id'])


def get_one_question(question_id):
    question_data = DAL.questions.select_one(question_id)
    question_data['comments'] = DAL.comments.get_comments_for_a_question(question_id)
    return question_data


def get_answer_with_its_question(answer_id):
    answer_data = DAL.answers.select_one(answer_id)
    question_data = DAL.questions.select_one(answer_data['question_id'])
    answer_data['question'] = question_data
    return answer_data


def get_comment_with_its_question(comment_id):
    comment_data = DAL.comments.select_one(comment_id)
    question_data = DAL.questions.select_one(comment_data['question_id'])
    answer_data = DAL.answers.select_one(comment_data['answer_id'])
    comment_data['question'] = question_data
    comment_data['answer'] = answer_data
    return comment_data


def get_answers_for_a_question(question_id):
    answers = DAL.answers.get_answers_for_a_question(question_id)
    return answers


def add_answer(question_id, request, upload_image_func, app, session):
    request_form = dict(request.form)
    session['id'] = DAL.users.get_one_user(session['username'])['id']
    __upload_file_if_any(request, request_form, upload_image_func, app)
    request_form['question_id'] = question_id
    DAL.answers.add_new(request_form, session['id'])


def edit_question(request, question_data, send_from_directory, app):
    form_request = dict(request.form)
    __delete_image(question_data, app)
    __upload_file_if_any(request, form_request, send_from_directory, app)
    form_request['view_number'] = question_data['view_number']
    form_request['vote_number'] = question_data['vote_number']
    form_request['id'] = question_data['id']
    DAL.questions.update(form_request)


def increase_view_number(question_data):
    question_data['view_number'] += 1
    DAL.questions.update(question_data)


def question_vote_up(question_id):
    question = DAL.questions.select_one(question_id)
    question['vote_number'] = question['vote_number'] + 1
    DAL.questions.update(question)


def question_vote_down(question_id):
    question = DAL.questions.select_one(question_id)
    question['vote_number'] = question['vote_number'] - 1
    DAL.questions.update(question)


def answer_vote_up(answer_id):
    answer = DAL.answers.select_one(answer_id)
    answer['vote_number'] = answer['vote_number'] + 1
    DAL.answers.update(answer)
    return answer['question_id']


def answer_vote_down(answer_id):
    answer = DAL.answers.select_one(answer_id)
    answer['vote_number'] = answer['vote_number'] - 1
    DAL.answers.update(answer)
    return answer['question_id']


def answer_accept(question_id, answer_id):
    DAL.accepted_answers.add(question_id, answer_id)


def delete_question(question_id, app):
    question = DAL.questions.select_one(question_id)
    question_answers = DAL.answers.get_answers_for_a_question(question_id)
    for answer in question_answers:
        __delete_image(answer, app)
    __delete_image(question, app)
    DAL.questions.delete(question)


def delete_answer(answer_id, app):
    answer = DAL.answers.select_one(answer_id)
    question_id = answer['question_id']
    __delete_image(answer, app)
    DAL.answers.delete(answer)
    return question_id


def edit_answer(request):
    edited_answer = dict(request)
    answer = DAL.answers.select_one(edited_answer['id'])
    edited_answer['vote_number'] = answer['vote_number']
    DAL.answers.update(edited_answer)
    return answer['question_id']


def edit_comment(request):
    edited_comment = dict(request)
    comment = DAL.comments.select_one(edited_comment['id'])
    if comment['edited_count']:
        edited_comment['edited_count'] = comment['edited_count'] + 1
    else:
        edited_comment['edited_count'] = 1
    current_time = time.time()
    edited_comment['submission_time'] = datetime.fromtimestamp(current_time)
    if comment['answer_id']:
        result = DAL.answers.get_question_id_from_answer(comment['answer_id'])
        comment['question_id'] = result['question_id']
    DAL.comments.update(edited_comment)
    return comment['question_id']


def comment_on_question(request, session):
    comment = dict(request.form)
    comment['answer_id'] = None
    session['id'] = DAL.users.get_one_user(session['username'])['id']
    DAL.comments.add_new(comment, session['id'])


def delete_comment(comment_id):
    comment = DAL.comments.delete_from_question(comment_id)
    if comment['question_id'] is not None:
        return comment['question_id']
    else:
        relevant_question = DAL.answers.select_one(comment['answer_id'])
        return relevant_question['question_id']


def comment_on_answer(request, session):
    comment = dict(request.form)
    comment['question_id'] = None
    session['id'] = DAL.users.get_one_user(session['username'])['id']
    DAL.comments.add_new(comment, session['id'])


def get_comments_for_answers(answers):
    for answer in answers:
        answer['comments'] = DAL.comments.get_comments_for_an_answer(answer['id'])


def add_tag(request):
    tag = dict(request.form)
    DAL.tags.add_new(tag)


def get_all_tags():
    tag_data = DAL.tags.get_all()
    return tag_data


def get_tags_for_question(question):
    question['tags'] = DAL.tags.get_all_for_a_question(question['id'])


def add_tag_to_question(request):
    tag = dict(request.form)
    DAL.tags.add_to_question(tag)


def remove_tag_from_question(question_id, tag_id):
    DAL.tags.remove_from_question(question_id, tag_id)


def register_a_user(request):
    username = request.form['username']
    passwd = hash_password(request.form['password'])
    data = {
        'user_name': username,
        'password': passwd
    }
    DAL.users.add_user(data)


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_login(request, session):
    hashed_bytes_password = DAL.users.get_password(request.form['username'])
    if hashed_bytes_password:
        is_success = bcrypt.checkpw(request.form['password'].encode('utf-8'), hashed_bytes_password['pw'].encode('utf-8'))
        session['username'] = request.form['username']
        session['id'] = DAL.users.get_one_user(session['username'])['id']
        return is_success


def __upload_file_if_any(form_request, item, send_from_directory, app):
    """
    Uploads the POST-ed file if the request contains an image.
    :param form_request: POST request from a HTML form.
    :param item: (dict) Question or an Answer entity.
    :return: (None) item['image'] key gets updated with the image ID.
    """

    if form_request.method != 'POST':
        item['image'] = ''
        return None

    if 'image' not in form_request.files:
        item['image'] = ''
        return None

    image = form_request.files['image']

    if image.filename == '':
        item['image'] = ''
        return None

    if image and __allowed_file(image.filename):
        file_extension = os.path.splitext(image.filename)[1]
        filename = str(uuid.uuid1()) + file_extension
        item['image'] = filename
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    item['image'] = ''


def __allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in __ALLOWED_EXTENSIONS


def __delete_image(item, app):
    """Remove image from the disk.

    :param item: (dict) Answer or Question entity.
    :return: (None
    """

    if item['image']:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item['image']))


def show_all_users():
    data = DAL.users.get_all_users()
    return data


def show_one_user(user_id):
    user_data = DAL.users.get_one_user(user_id)
    return user_data


def get_tags_with_questions():
    sql_data = DAL.tags.get_tags_with_questions()
    data = {}
    for item in sql_data:
        if item['name'] not in data:
            data[item['name']] = [item]
        else:
            data[item['name']] += [item]
    return data


def is_logged_in(session):
    return '' != session['username']
