# Imports
from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import config

# App configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret
app.config['SQLALCHEMY_DATABASE_URI'] = config.db_uri

# Initialize DB
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    displayName = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.displayName}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.user_id}', {self.title}', '{self.datePosted}')"


# Register index route
@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('pages/index.html')

# Register registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('pages/register.html', title='Register', form=form)

# Register login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if True: # This should check if username and password in db
            flash(f'You have successfully loged in as {form.username.data}', 'success')
            return redirect(url_for('index'))
        else:
            flash('Username and password combination incorrect', 'danger')
    return render_template('pages/login.html', title='Login', form=form)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
