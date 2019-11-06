from flask import Flask, render_template, request, redirect, send_from_directory, url_for

import data_handler
import os
import util
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/images/'

saved_data = {}


@app.route('/')
@app.route('/list')
def show_questions():
    result_data = data_handler.route_list(request)
    return render_template('question/display_all.html', questions=result_data[0], order_direction=result_data[1])


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        data_handler.add_question(request,send_from_directory, app)
        return redirect('/list')
    return render_template('question/create.html')


@app.route('/question/<int:question_id>')
def show_answers(question_id):
    question_data = data_handler.get_one_question(question_id)
    answers = data_handler.get_answers_for_a_question(question_id)
    return render_template('question/display_one.html', question=question_data, current_answers=answers)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_new_answer(question_id):
    pass


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question_data = data_handler.get_one_question(question_id)
    if request.method == 'POST':
        data_handler.edit_question(request, question_data, send_from_directory, app)
        return redirect(url_for('show_answers', question_id=question_id))
    return render_template('question/edit.html',
                           title='Edit Question',
                           question_id=question_id,
                           question_data=question_data)


@app.route('/question/<question_id>/vote-up')
def question_vote_up(question_id):
    data_handler.question_vote_up(question_id)
    return redirect('/list')


@app.route('/question/<question_id>/vote-down')
def question_vote_down(question_id):
    data_handler.question_vote_down(question_id)
    return redirect('/')


@app.route('/answer/<answer_id>/vote_up')
def answer_vote_up(answer_id):
    pass


@app.route('/answer/<answer_id>/vote_down')
def answer_vote_down(answer_id):
    pass


@app.route('/question/<int:question_id>/deleteendpoint')
def delete_question(question_id):
    pass


@app.route('/answer/<int:answer_id>/delete')
def delete_answer(answer_id):
    question_id = data_handler.delete_answer(answer_id, app)
    return redirect(url_for('show_answers', question_id=question_id))


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
