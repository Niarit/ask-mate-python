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
    return render_template('add.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
