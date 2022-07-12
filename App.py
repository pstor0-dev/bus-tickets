from re import RegexFlag
from flask import Flask, render_template, url_for, redirect, request
import sqlite3

# Flask
app = Flask(__name__)

# DataBase
con = sqlite3.connect('database.db', check_same_thread=False)
cur = con.cursor()

@app.route("/", methods=['GET', 'POST'])
def index_page_processor():
    return render_template('login.html')

@app.route("/login", methods=['GET', 'POST'])
def login_page_processor():
    return render_template('login.html')

@app.route("/registration", methods=['GET', 'POST'])
def registration_page_processor():
    if request.method == 'POST':
        reg_email = request.form['registerFormEmail']
        reg_pass = request.form['registerFormPassword']

        cur.execute('SELECT * FROM users WHERE email = ?', [reg_email])
        con.commit()
        user = cur.fetchall()
        
        # Checking if the user is registered
        if user == []:
            # Password length check
            if len(reg_pass) < 8:
                return 'The password is too short.'
            elif len(reg_pass) > 32:
                return 'The password is too long.'

            cur.execute('INSERT INTO users (email, pass) VALUES (?, ?)', (reg_email, reg_pass))
            con.commit()
            return '<p>Account created successfully! <a href="/login">Sign In</a></p>'
        else:
            return '<p>This email address is busy. <a href="/registration">Return</a></p>'

    return render_template('registration.html')

# Static files loaders
@app.route('/style.css')
def custom_css_loading():
    return redirect(url_for('static', filename='css/style.css'))