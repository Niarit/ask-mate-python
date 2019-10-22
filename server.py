from flask import Flask, render_template, request, redirect, url_for

import data_handler

app = Flask(__name__)

saved_data = {}


@app.route('/')
@app.route('/list')
def route_list():
    questions = data_handler.get_all_data('question.csv',break_lines=True)
    return render_template('list.html', questions=questions)


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
    questions = data_handler.get_all_data('question.csv', True)
    title = ''.join([question['title'] for question in questions if question['id'] == question_id])
    answers = data_handler.get_all_data('answer.csv', True)
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
    questions = data_handler.get_all_data('question.csv', True)
    title = ''.join([question['title'] for question in questions if question['id'] == question_id])
    return render_template('new_answer.html', title=title, question_id=question_id)

@app.route('/question/<question_id>/edit', methods=['GET','POST'])
def edit_question(question_id):
    if request.method == 'POST':
        question_data = {
            'id': question_id,
            'title': request.form.get('title'),
            'message': request.form.get('message'),
        }
        data_handler.edit_question(question_data, 'question.csv')
        return redirect('/list')
    question_data = data_handler.get_id(question_id)
    return render_template()


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
