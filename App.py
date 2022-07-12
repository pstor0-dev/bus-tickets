from flask import Flask, make_response, render_template, url_for, redirect, request
import sqlite3

# Flask
app = Flask(__name__)

# DataBase
con = sqlite3.connect('database.db', check_same_thread=False)
cur = con.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, pass TEXT (32), balance INTEGER (1000000) DEFAULT (0))')
con.commit()

@app.route('/', methods=['GET', 'POST'])
def index_page_processor():
    if request.method == 'POST':
        form_email = request.form['loginFormEmail']
        form_pass = request.form['loginFormPassword']

        cur.execute('SELECT * FROM users WHERE email = ?', [form_email])
        con.commit()
        user = cur.fetchone()
        
        # Checking if the user is registered
        if user == []:
            return '<p>User is not found. <a href="/">Return</a></p>'
        else:
            if form_pass == user[2]:
                resp = make_response(redirect('/profile'))
                resp.set_cookie('logged_email', form_email)
                resp.set_cookie('logged_status', 'True')
                return resp
            else:
                return '<p>Invalid password. <a href="/">Return</a></p>'
    else:
        return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page_processor():
    if request.method == 'POST':
        form_email = request.form['loginFormEmail']
        form_pass = request.form['loginFormPassword']

        cur.execute('SELECT * FROM users WHERE email = ?', [form_email])
        con.commit()
        user = cur.fetchone()
        
        # Checking if the user is in the database
        if user == []:
            return '<p>User is not found. <a href="/login">Return</a></p>'
        else:
            if form_pass == user[2]: # Checking if the password is correct
                resp = make_response(redirect('/profile'))
                resp.set_cookie('logged_email', form_email)
                resp.set_cookie('logged_status', 'True')
                return resp
            else:
                return '<p>Invalid password. <a href="/login">Return</a></p>'
    else:
        return render_template('login.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration_page_processor():
    if request.method == 'POST':
        form_email = request.form['registerFormEmail']
        form_pass = request.form['registerFormPassword']

        cur.execute('SELECT * FROM users WHERE email = ?', [form_email])
        con.commit()
        user = cur.fetchall()
        
        # Checking if the user is registered
        if user == []:
            # Password length check
            if len(form_pass) < 8:
                return 'The password is too short.'
            elif len(form_pass) > 32:
                return 'The password is too long.'

            cur.execute('INSERT INTO users (email, pass) VALUES (?, ?)', (form_email, form_pass))
            con.commit()
            return '<p>Account created successfully! <a href="/login">Sign In</a></p>'
        else:
            return '<p>This email address is busy. <a href="/registration">Return</a></p>'
    else:
        return render_template('registration.html')

@app.route('/profile', methods=['GET'])
def profile_page_processor(balance=None):
    if request.cookies.get('logged_status') == 'True':
        logged_email = request.cookies.get('logged_email')

        cur.execute('SELECT * FROM users WHERE email = ?', [logged_email])
        con.commit()
        user = cur.fetchone()

        balance = user[3]

        return render_template('profile.html', balance=balance)
    else:
        return '<p><a href="/login">Login</a> to access your profile.</p>'

@app.route('/logout', methods=['GET'])
def logout_page_processor():
    if request.cookies.get('logged_status') == 'True':
        resp = make_response(redirect('/'))
        resp.delete_cookie('logged_status')
        resp.delete_cookie('logged_email')
        return resp

# Static files loaders
@app.route('/style.css')
def custom_css_loading():
    return redirect(url_for('static', filename='css/style.css'))