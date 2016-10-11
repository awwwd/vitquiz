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
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_check', methods = ['POST'])
def login_check():
    error = None
    if request.method == 'POST':
        exists = g.db.execute('select * from students where reg = ? and password = ?', [request.form['regno'], request.form['password']])
        l = exists.fetchall()
        if len(l):
            session['id']=l[0][0]
            return redirect(url_for('index'))
        else:
            return render_template("login.html", error=True)
    return error


@app.route("/signup_entry", methods = ['POST'])
def signup_entry():
    error = None
    if request.method == 'POST':
        exists = g.db.execute('select * from students where email = ?',[request.form['email']])
        if len(exists.fetchall()):
            return render_template('signup.html', error=True)
        else:
            g.db.execute('insert into students (fname,lname,reg,password,email) values (?,?,?,?,?)',[request.form['first_name'],request.form['last_name'],request.form['regno'],request.form['password'],request.form['email']])
            g.db.commit()
            return redirect(url_for('login'))
    return error

if __name__ == '__main__':
    app.run(debug=True)