from flask import Flask, render_template, request, redirect, url_for, session
from flask_babel import Babel, gettext
import random
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Лучше заменить на безопасный ключ из переменных окружения

# Конфигурация Flask-Babel
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'ru']
babel = Babel(app)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])

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
            answer = float(request.form['answer'])
            if 'start_time' in session and time.time() - session['start_time'] > 10:
                session['score'] -= 5
                session['message'] = gettext("Time's up!")
            else:
                if answer == session.get('correct_answer'):
                    session['score'] += 10
                    session['correct_answers'] += 1
                    session['message'] = gettext("Correct!")
                else:
                    session['score'] -= 5
                    session['message'] = gettext("Incorrect!")
        except (ValueError, KeyError):
            session['score'] -= 5
            session['message'] = gettext("Invalid input. Incorrect!")
        
        session['total_questions'] += 1
        return redirect(url_for('child'))
    
    num1 = random.randint(1, 99)
    num2 = random.randint(1, 99)
    operation = random.choice(['+', '-', '*', '/'])
    
    if operation == '+':
        session['correct_answer'] = num1 + num2
    elif operation == '-':
        session['correct_answer'] = num1 - num2
    elif operation == '*':
        session['correct_answer'] = num1 * num2
    elif operation == '/':
        session['correct_answer'] = round(num1 / num2, 2)
    
    session['start_time'] = time.time()
    return render_template('child.html', num1=num1, num2=num2, operation=operation, score=session['score'], message=session['message'])

if __name__ == '__main__':
    app.run(debug=True)
