from flask import Flask, render_template, request, redirect, url_for, session
import random
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/parent')
def parent():
    return render_template('parent.html', 
                           total_questions=session.get('total_questions', 0),
                           correct_answers=session.get('correct_answers', 0),
                           score=session.get('score', 0))

@app.route('/child', methods=['GET', 'POST'])
def child():
    if 'score' not in session:
        session['score'] = 0
    if 'correct_answers' not in session:
        session['correct_answers'] = 0
    if 'total_questions' not in session:
        session['total_questions'] = 0
    if 'message' not in session:
        session['message'] = ''

    if request.method == 'POST':
        try:
            answer = int(request.form['answer'])
            if 'start_time' in session and time.time() - session['start_time'] > 10:
                session['score'] -= 5
                session['message'] = "Время вышло!"
            else:
                if answer == session.get('correct_answer'):
                    session['score'] += 10
                    session['correct_answers'] += 1
                    session['message'] = "Правильно!"
                else:
                    session['score'] -= 5
                    session['message'] = "Неправильно!"
        except (ValueError, KeyError):
            session['score'] -= 5
            session['message'] = "Неверный ввод. Неправильно!"

        session['total_questions'] += 1
        return redirect(url_for('child'))

    num1 = random.randint(10, 99)
    num2 = random.randint &#8203;:citation[oaicite:0]{index=0}&#8203;
