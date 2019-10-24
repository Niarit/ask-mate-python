from flask import Flask, render_template, request, redirect, send_from_directory, url_for

import data_handler
import os
import util
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/images/'

saved_data = {}
__ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@app.route('/')
@app.route('/list')
def route_list():
    questions = data_handler.get_data('questions')
    should_reverse = True
    if request.args.get('order_direction') == 'asc':
        should_reverse = False
    column_name = 'submission_time'
    if request.args.get('order_by'):
        column_name = request.args.get('order_by')
    sorted_questions = sorted(questions, key=lambda question: util.__preformat_for_sort(question[column_name]), reverse=should_reverse)
    order_direction = 'desc'
    if should_reverse:
        order_direction = 'asc'
    return render_template('list.html', questions=sorted_questions, order_direction=order_direction)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        for item in request.form:
            saved_data[item] = request.form[item]
        __upload_file_if_any(request, saved_data)
        data_handler.add_new_question(saved_data)
        return redirect('/list')
    return render_template('add.html',)


@app.route('/question/<question_id>')
def show_answers(question_id):
    question_id = int(question_id)
    questions = data_handler.get_data('questions')
    question_row_index = data_handler.get_row_index_by_id(question_id, questions)
    question = questions[question_row_index]
    answers = data_handler.get_data('answers')
    answers_for_question = [answer for answer in answers if answer['question_id'] == question_id]
    return render_template('answer.html',
                           question=question,
                           current_answers=answers_for_question)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_new_answer(question_id):
    if request.method == 'POST':
        answer = dict(request.form)
        answer['question_id'] = question_id
        __upload_file_if_any(request, answer)
        data_handler.insert_answer(answer)
        return redirect(f'/question/{question_id}')
    questions = data_handler.get_data('questions')
    title = ''.join([question['title'] for question in questions if question['id'] == question_id])
    return render_template('new_answer.html', title=title, question_id=question_id)


@app.route('/question/<question_id>/edit', methods=['GET','POST'])
def edit_question(question_id):
    all_questions = data_handler.get_data('questions')
    question_index = data_handler.get_row_index_by_id(question_id, all_questions)
    question_data = all_questions[question_index]
    if request.method == 'POST':
        question_data['title'] = request.form.get('title')
        question_data['message'] = request.form.get('message')
        __delete_image(question_data)
        __upload_file_if_any(request, question_data)
        data_handler.update_existing_file(all_questions, 'question.csv', data_handler.QUESTION_HEADERS)
        return redirect(url_for('show_answers', question_id=question_id))
    return render_template('edit_question.html',
                           title='Edit Question',
                           question_id=question_id,
                           question_data=question_data)


@app.route('/question/<question_id>/vote-up')
def question_vote_up(question_id):
    questions = data_handler.get_data('questions')
    for question in questions:
        if question['id'] == int(question_id):
            question['vote_number'] = question['vote_number'] + 1
    data_handler.question_vote_update(questions)
    return redirect('/list')


@app.route('/question/<question_id>/vote-down')
def question_vote_down(question_id):
    questions = data_handler.get_data('questions')
    for question in questions:
        if question['id'] == int(question_id):
            question['vote_number'] = question['vote_number'] - 1
    data_handler.question_vote_update(questions)
    return redirect('/')


@app.route('/answer/<answer_id>/vote_up')
def answer_vote_up(answer_id):
    answer = util.vote_answer(answer_id, lambda vote_number: vote_number + 1)
    return redirect(f'/question/{answer["question_id"]}')


@app.route('/answer/<answer_id>/vote_down')
def answer_vote_down(answer_id):
    answer = util.vote_answer(answer_id, lambda vote_number: vote_number - 1)
    return redirect(f'/question/{answer["question_id"]}')


@app.route('/question/<int:question_id>/deleteendpoint')
def delete_question(question_id):
    questions = data_handler.get_data('questions')
    question_row_index = data_handler.get_row_index_by_id(question_id, questions)
    answers = data_handler.get_data('answers')
    for answer in answers:
        if answer['question_id'] == question_id:
            delete_answer(answer['id'])
    __delete_image(questions[question_row_index])
    questions.pop(question_row_index)
    data_handler.save_questions(questions)
    return redirect('/list')


@app.route('/answer/<int:answer_id>/delete')
def delete_answer(answer_id):
    question_id = request.args.get('question_id')
    answers = data_handler.get_data('answers')
    answer_row_index = data_handler.get_row_index_by_id(answer_id, answers)
    __delete_image(answers[answer_row_index])
    answers.pop(answer_row_index)
    data_handler.save_answers(answers)
    return redirect(f'/question/{question_id}')


def __upload_file_if_any(form_request, item):
    """
    Uploads the POST-ed file if the request contains an image.
    :param form_request: POST request from a HTML form.
    :param item: (dict) Question or an Answer entity.
    :return: (None) item['image'] key gets updated with the image ID.
    """

    if form_request.method != 'POST':
        return None

    if 'image' not in form_request.files:
        return None

    image = form_request.files['image']

    if image.filename == '':
        return None

    if image and __allowed_file(image.filename):
        file_extension = os.path.splitext(image.filename)[1]
        filename = str(uuid.uuid1()) + file_extension
        item['image'] = filename
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def __allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in __ALLOWED_EXTENSIONS


def __delete_image(item):
    """Remove image from the disk.

    :param item: (dict) Answer or Question entity.
    :return: (None
    """

    if item['image']:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item['image']))


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
