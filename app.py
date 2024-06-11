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
    # Инициализация переменных в сессии, если они отсутствуют
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
                session['message'] = "Time's up!"
            else:
                if answer == session.get('correct_answer'):
                    session['score'] += 10
                    session['correct_answers'] += 1
                    session['message'] = "Correct!"
                else:
                    session['score'] -= 5
                    session['message'] = "Wrong!"
        except (ValueError, KeyError):
            session['score'] -= 5
            session['message'] = "Invalid input. Wrong!"

        session['total_questions'] += 1
        return redirect(url_for('child'))

    num1 = random.randint(10, 99)
    num2 = random.randint(10, 99)
    operation = random.choice(['+', '-', '*', '/'])

    if operation == '+':
        correct_answer = num1 + num2
    elif operation == '-':
        correct_answer = num1 - num2
    elif operation == '*':
        correct_answer = num1 * num2
    elif operation == '/':
        while num2 == 0 or num1 % num2 != 0:
            num2 = random.randint(10, 99)
        correct_answer = num1 // num2

    wrong_answers = set()
    while len(wrong_answers) < 3:
        wrong_answer = correct_answer + random.choice([-10, -5, 5, 10])
        if wrong_answer != correct_answer and wrong_answer not in wrong_answers:
            wrong_answers.add(wrong_answer)
    wrong_answers = list(wrong_answers)

    options = [correct_answer] + wrong_answers
    random.shuffle(options)

    session['correct_answer'] = correct_answer
    session['start_time'] = time.time()

    return render_template('child.html', num1=num1, num2=num2, operation=operation, options=options, message=session.get('message'))

if __name__ == "__main__":
    app.run(debug=True)
