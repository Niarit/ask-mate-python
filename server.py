from flask import Flask, render_template, request, redirect, send_from_directory, url_for, session

import data_handler
import util
from functools import wraps

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/images/'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def only_authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not data_handler.is_logged_in(session):
            return redirect(url_for('login_user'))
        return f(*args, **kws)
    return decorated_function


@app.route('/')
def show_five_question():
    questions = data_handler.route_five_list()
    if 'username' not in session:
        session['username'] = ''
    return render_template('question/display_five.html', questions=questions, username=session['username'])


@app.route('/add-question', methods=['GET', 'POST'])
@only_authenticated
def add_question():
    if request.method == 'POST':
        data_handler.add_question(request, send_from_directory, app, session)
        return redirect('/list')
    return render_template('question/create.html', username=session['username'])


@app.route('/list')
def show_questions():
    result_data = data_handler.route_list(request)
    return render_template('question/display_all.html', questions=result_data[0], order_direction=result_data[1],
                           username=session['username'])


@app.route('/question/<int:question_id>')
def show_answers(question_id):
    question_data = data_handler.get_one_question(question_id)
    data_handler.get_tags_for_question(question_data)
    data_handler.increase_view_number(question_data)
    answers = data_handler.get_answers_for_a_question(question_id)
    data_handler.get_comments_for_answers(answers)
    return render_template('question/display_one.html', question=question_data, current_answers=answers,
                           username=session['username'])


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
@only_authenticated
def add_new_answer(question_id):
    if request.method == 'POST':
        data_handler.add_answer(question_id, request, send_from_directory, app, session)
        return redirect(url_for('show_answers', question_id=question_id))
    question_data = data_handler.get_one_question(question_id)
    return render_template('answer/create.html', question=question_data, username=session['username'])


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
@only_authenticated
def edit_question(question_id):
    question_data = data_handler.get_one_question(question_id)
    if request.method == 'POST':
        data_handler.edit_question(request, question_data, send_from_directory, app)
        return redirect(url_for('show_answers', question_id=question_id))
    return render_template('question/edit.html',
                           title='Edit Question',
                           question_id=question_id,
                           question_data=question_data,
                           username=session['username'])


@app.route('/question/<question_id>/vote-up')
@only_authenticated
def question_vote_up(question_id):
    data_handler.question_vote_up(question_id)
    return redirect(request.referrer)


@app.route('/question/<question_id>/vote-down')
@only_authenticated
def question_vote_down(question_id):
    data_handler.question_vote_down(question_id)
    return redirect(request.referrer)


@app.route('/answer/<answer_id>/vote_up')
@only_authenticated
def answer_vote_up(answer_id):
    answer = data_handler.answer_vote_up(answer_id)
    return redirect(url_for('show_answers', question_id=answer))


@app.route('/answer/<answer_id>/vote_down')
@only_authenticated
def answer_vote_down(answer_id):
    answer = data_handler.answer_vote_down(answer_id)
    return redirect(url_for('show_answers', question_id=answer))


@app.route('/question/<int:question_id>/answer/<int:answer_id>/accept')
@only_authenticated
def answer_accept(question_id, answer_id):
    data_handler.answer_accept(question_id, answer_id)
    return redirect(request.referrer)


@app.route('/question/<int:question_id>/delete')
@only_authenticated
def delete_question(question_id):
    data_handler.delete_question(question_id, app)
    return redirect(url_for('show_questions'))


@app.route('/answer/<int:answer_id>/delete')
@only_authenticated
def delete_answer(answer_id):
    question_id = data_handler.delete_answer(answer_id, app)
    return redirect(url_for('show_answers', question_id=question_id))


@app.route('/search')
def search():
    result = data_handler.search(request)
    return render_template('search/search_result.html', questions=result, phrase=request.args.get('q'),
                           username=session['username'])


@app.route('/answer/<int:answer_id>/edit', methods=['GET', 'POST'])
@only_authenticated
def edit_answer(answer_id):
    if request.method == 'POST':
        question_id = data_handler.edit_answer(request.form)
        return redirect(url_for('show_answers', question_id=question_id))
    answer = data_handler.get_answer_with_its_question(answer_id)
    return render_template('answer/edit.html', answer=answer, username=session['username'])


@app.route('/comments/<int:comment_id>/edit', methods=['GET', 'POST'])
@only_authenticated
def edit_comment(comment_id):
    if request.method == 'POST':
        question_id = data_handler.edit_comment(request.form)
        return redirect(url_for('show_answers', question_id=question_id))
    comment = data_handler.get_comment_with_its_question(comment_id)
    return render_template('comment/edit.html', comment=comment, username=session['username'])


@app.route('/question/<int:question_id>/new-comment', methods=['GET', 'POST'])
@only_authenticated
def comment_on_question(question_id):
    question_data = data_handler.get_one_question(question_id)
    if request.method == 'POST':
        data_handler.comment_on_question(request, session)
        return redirect(url_for('show_answers', question_id=question_id))
    return render_template('comment/create_for_question.html', question=question_data, username=session['username'])


@app.route('/comments/<comment_id>/delete')
@only_authenticated
def delete_comment(comment_id):
    question_id = data_handler.delete_comment(comment_id)
    return redirect(url_for('show_answers', question_id=question_id))


@app.route('/answer/<int:answer_id>/new-comment', methods=['GET', 'POST'])
@only_authenticated
def comment_on_answer(answer_id):
    answer_data = data_handler.get_answer_with_its_question(answer_id)
    if request.method == 'POST':
        data_handler.comment_on_answer(request, session)
        return redirect(url_for('show_answers', question_id=answer_data['question_id']))
    return render_template('comment/create_for_answer.html', answer=answer_data, username=session['username'])


@app.route('/tag', methods=['GET', 'POST'])
@only_authenticated
def create_tag():
    if request.method == 'POST':
        data_handler.add_tag(request)
        return redirect(request.referrer)
    tags_data = data_handler.get_all_tags()
    return render_template('tag/create.html', tags=tags_data, username=session['username'])


@app.route('/question/<int:question_id>/new-tag', methods=['GET', 'POST'])
@only_authenticated
def add_tag(question_id):
    if request.method == 'POST':
        data_handler.add_tag_to_question(request)
        return redirect(url_for('show_answers', question_id=question_id))
    question_data = data_handler.get_one_question(question_id)
    tags_data = data_handler.get_all_tags()
    return render_template('tag/add_to_question.html', question=question_data, tags=tags_data,
                           username=session['username'])


@app.route('/question/<int:question_id>/tag/<int:tag_id>/delete')
@only_authenticated
def remove_tag_from_question(question_id, tag_id):
    data_handler.remove_tag_from_question(question_id, tag_id)
    return redirect(request.referrer)


@app.route('/registration', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        data_handler.register_a_user(request)
        return redirect(url_for('show_questions'))
    return render_template('user/reg.html', username=session['username'])


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        if data_handler.verify_login(request, session):
            return redirect(url_for('show_five_question'))
    return render_template('user/login.html', username=session['username'])


@app.route('/logout')
def logout():
    session['username'] = ''
    session['id'] = ''
    return redirect(url_for('show_five_question'))


@app.template_filter('pretty_time')
def pretty_datetime_for_ui_filter(datetime):
    return util.pretty_datetime_for_ui(datetime)


@app.context_processor
def highlight_phrase():
    return util.highlight_phrase()


@app.route('/all-users')
def show_all_users():
    data = data_handler.show_all_users()
    return render_template('user/all_users.html', data=data, username=session['username'])


@app.route('/user/<user_id>')
@only_authenticated
def show_user_page(user_id):
    user_data = data_handler.show_one_user(user_id)
    users_question = data_handler.get_users_questions(session)
    users_answers = data_handler.get_users_answers(session)
    users_question_comments = data_handler.get_users_comments(session)[1]
    users_answer_comments = data_handler.get_users_comments(session)[0]
    user_rep = data_handler.get_user_reputation(session)
    return render_template('user/user_page.html',
                           data=user_data,
                           user_questions=users_question,
                           user_answers=users_answers,
                           user_q_comments=users_question_comments,
                           users_a_comments=users_answer_comments,
                           user_rep=user_rep)


@app.route('/tags')
def show_tags():
    tag_data = data_handler.get_tags_with_questions()
    return render_template('tag/display_all.html', data=tag_data, username=session['username'])


@app.context_processor
def is_logged():
    return dict(is_logged_in=data_handler.is_logged_in(session))


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )

