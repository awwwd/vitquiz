from flask import Flask, render_template, g, request, url_for, redirect, session
import sqlite3
import os

DATABASE = 'data.db'
DEBUG = True
SECRET_KEY = 'amaroporanojahachai'

app = Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'data.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('VITQuiz_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()
    print 'sucess'

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    if bool(session.get('id')):
        return redirect(url_for('home'))
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('profile.html', name = session.get('reg'), logged = True)

@app.route('/login_check', methods = ['GET', 'POST'])
def login_check():
    error = None
    if request.method == 'POST':
        exists = g.db.execute('select * from students where reg = ? and password = ?',[request.form['regno'],request.form['password']])
        print exists
        l = exists.fetchall()
        print l
        if len(l) > 0:
            session['reg'] = l[0][2]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error = True)

if __name__ == '__main__':
    app.run(debug=True)