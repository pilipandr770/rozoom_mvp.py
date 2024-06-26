from flask import Flask, render_template, request, redirect, url_for, session
import random
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Лучше заменить на безопасный ключ из переменных окружения

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
                session['message'] = "Zeit ist um!"
            else:
                if answer == session.get('correct_answer'):
                    session['score'] += 10
                    session['correct_answers'] += 1
                    session['message'] = "Richtig!"
                else:
                    session['score'] -= 5
                    session['message'] = "Falsch!"
        except (ValueError, KeyError):
            session['score'] -= 5
            session['message'] = "Ungültige Eingabe. Falsch!"
        
        session['total_questions'] += 1
        return redirect(url_for('child'))
    
    num1 = random.randint(1, 99)
    num2 = random.randint(1, 99)
    operation = random.choice(['+', '-', '*', '/'])
    
    if operation == '+':
        correct_answer = num1 + num2
    elif operation == '-':
        correct_answer = num1 - num2
    elif operation == '*':
        correct_answer = num1 * num2
    elif operation == '/':
        correct_answer = round(num1 / num2, 2)
    
    session['correct_answer'] = correct_answer
    session['start_time'] = time.time()
    
    wrong_answers = [correct_answer + random.randint(-10, 10) for _ in range(3)]
    options = wrong_answers + [correct_answer]
    random.shuffle(options)
    
    return render_template('child.html', num1=num1, num2=num2, operation=operation, options=options, score=session['score'], message=session['message'])

if __name__ == '__main__':
    app.run(debug=True)
