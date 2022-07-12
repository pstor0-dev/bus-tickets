from flask import Flask, render_template, url_for, redirect

# Flask
app = Flask(__name__)

@app.route("/")
def index_page_processor():
    return render_template('login.html')

@app.route("/login")
def login_page_processor():
    return render_template('login.html')

@app.route("/registration")
def registration_page_processor():
    return render_template('registration.html')

# Static files loaders
@app.route('/style.css')
def custom_css_loading():
    return redirect(url_for('static', filename='css/style.css'))