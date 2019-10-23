from flask import Flask, render_template, request, redirect, url_for

import data_handler
import util

app = Flask(__name__)

saved_data = {}


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
        data_handler.add_new_question(saved_data)
        return redirect('/list')
    return render_template('add.html',)


@app.route('/question/<question_id>')
def show_answers(question_id):
    question_id = int(question_id)
    questions = data_handler.get_data('questions')
    title = ''.join([question['title'] for question in questions if question['id'] == question_id])
    answers = data_handler.get_data('answers')
    answers_for_question = [answer for answer in answers if answer['question_id'] == question_id]
    return render_template('answer.html',
                           question_title=title,
                           current_answers=answers_for_question,
                           question_id=question_id)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_new_answer(question_id):
    if request.method == 'POST':
        data_handler.add_new_message(request.form, question_id)
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
        data_handler.update_existing_file(all_questions, data_handler.QUESTION_DATA_PATH, data_handler.QUESTION_HEADERS)
        return redirect('/list')
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


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
